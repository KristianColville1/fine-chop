from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, OrderLineItem
from menu.models import MenuItem
from profiles.models import Profile
import json
import time
import stripe


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Private method sends users a confirmation email
        """
        their_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt', {
                'order': order,
                'contact_email': settings.DEFAULT_FROM_EMAIL
            })

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [their_email])

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details  # updated
        ship_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)  # updated

        # Clean data in the shipping details
        for field, value in ship_details.address.items():
            if value == "":
                ship_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = Profile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = ship_details.phone
                profile.default_country = ship_details.address.country
                profile.default_postcode = ship_details.address.postal_code
                profile.default_town_or_city = ship_details.address.city
                profile.default_street_address1 = ship_details.address.line1
                profile.default_street_address2 = ship_details.address.line2
                profile.default_county = ship_details.address.state
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=ship_details.name,
                    user_profile=profile,
                    email__iexact=billing_details.email,
                    phone_number__iexact=ship_details.phone,
                    country__iexact=ship_details.address.country,
                    postcode__iexact=ship_details.address.postal_code,
                    town_or_city__iexact=ship_details.address.city,
                    street_address1__iexact=ship_details.address.line1,
                    street_address2__iexact=ship_details.address.line2,
                    county__iexact=ship_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified order already in database'),
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=ship_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=ship_details.phone,
                    country=ship_details.address.country,
                    postcode=ship_details.address.postal_code,
                    town_or_city=ship_details.address.city,
                    street_address1=ship_details.address.line1,
                    street_address2=ship_details.address.line2,
                    county=ship_details.address.state,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(cart).items():
                    menu_item = MenuItem.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            menu_item=menu_item,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data[
                                'menu_items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                menu_item=menu_item,
                                quantity=quantity,
                                portion_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Created order in webhook'),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(content=f'Webhook received: {event["type"]}',
                            status=200)

import os
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def get_checkout(request):
    """
    Get checkout page
    """
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in the cart!")
        return redirect(reverse('menu'))
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': os.environ.get("STRIPE_PUBLIC_KEY"),
        'client_secret': 'test client secret',
    }
    return render(request, template, context)
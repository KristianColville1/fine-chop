# Generated by Django 3.2.16 on 2022-11-27 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='seating_amount',
            field=models.IntegerField(default=2),
        ),
    ]
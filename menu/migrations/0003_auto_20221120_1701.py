# Generated by Django 3.2.16 on 2022-11-20 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20221120_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='updated_on',
        ),
    ]
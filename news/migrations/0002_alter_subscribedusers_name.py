# Generated by Django 3.2.16 on 2023-01-02 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribedusers',
            name='name',
            field=models.CharField(default='no username', max_length=100),
        ),
    ]

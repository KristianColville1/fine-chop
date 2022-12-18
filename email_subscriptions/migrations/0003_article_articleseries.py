# Generated by Django 3.2.16 on 2022-11-28 06:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import email_subscriptions.models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('email_subscriptions', '0002_auto_20221128_0642'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, default='', max_length=200)),
                ('slug', models.SlugField(unique=True, verbose_name='Series slug')),
                ('published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date published')),
                ('image', models.ImageField(default='default/no_image.jpg', max_length=255, upload_to=email_subscriptions.models.ArticleSeries.image_upload_to)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='profiles.profile')),
            ],
            options={
                'verbose_name_plural': 'Series',
                'ordering': ['-published'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, default='', max_length=200)),
                ('article_slug', models.SlugField(unique=True, verbose_name='Article slug')),
                ('content', tinymce.models.HTMLField(blank=True, default='')),
                ('notes', tinymce.models.HTMLField(blank=True, default='')),
                ('published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date published')),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('image', models.ImageField(default='default/no_image.jpg', max_length=255, upload_to=email_subscriptions.models.Article.image_upload_to)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='profiles.profile')),
                ('series', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='email_subscriptions.articleseries', verbose_name='Series')),
            ],
            options={
                'verbose_name_plural': 'Article',
                'ordering': ['-published'],
            },
        ),
    ]
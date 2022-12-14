# Generated by Django 3.2.16 on 2023-01-02 17:26

import contact.file_size
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=320)),
                ('contact_number', models.IntegerField()),
                ('message', models.TextField()),
                ('resume', models.FileField(upload_to='static/resumes/', validators=[contact.file_size.file_size])),
                ('application_number', models.CharField(default='', max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Job Applications',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='UserQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=320)),
                ('comment', models.TextField()),
                ('user_query_number', models.CharField(default='', max_length=254)),
                ('is_open', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'User Queries',
            },
        ),
        migrations.CreateModel(
            name='QueryResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField()),
                ('resolved', models.BooleanField(default=False)),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_query_response', to='contact.userquery')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplicationResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField()),
                ('is_successful', models.BooleanField(default=False)),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_application', to='contact.jobapplication')),
            ],
        ),
    ]

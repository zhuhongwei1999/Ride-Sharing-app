# Generated by Django 4.1.5 on 2023-02-06 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0002_searchrequest_ride_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchrequest',
            name='ride_request',
        ),
    ]
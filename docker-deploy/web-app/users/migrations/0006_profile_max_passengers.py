# Generated by Django 4.1.5 on 2023-02-03 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_vehicle_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='max_passengers',
            field=models.CharField(blank=True, default='', max_length=2),
        ),
    ]
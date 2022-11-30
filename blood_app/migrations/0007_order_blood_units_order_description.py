# Generated by Django 4.0.4 on 2022-05-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_app', '0006_blood_donation_recieve_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='blood_units',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]

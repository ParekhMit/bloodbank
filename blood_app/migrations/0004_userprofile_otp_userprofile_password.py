# Generated by Django 4.0.4 on 2022-05-23 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_app', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='otp',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

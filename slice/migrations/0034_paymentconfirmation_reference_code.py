# Generated by Django 4.2.4 on 2023-09-19 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slice', '0033_paymentconfirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentconfirmation',
            name='reference_code',
            field=models.CharField(default='N/A', max_length=8, unique=True),
        ),
    ]

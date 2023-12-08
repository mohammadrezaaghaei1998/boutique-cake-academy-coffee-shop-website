# Generated by Django 4.2.4 on 2023-09-09 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slice', '0015_cartitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]

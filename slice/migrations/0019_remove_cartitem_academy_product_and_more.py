# Generated by Django 4.2.4 on 2023-09-11 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slice', '0018_cartitem_course_cartitem_userinformation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='academy_product',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='coffee_delivery',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product_type',
            field=models.CharField(choices=[('academy_product', 'Academy Product'), ('coffee_delivery', 'Coffee Delivery')], default='academy_product', max_length=20),
        ),
    ]

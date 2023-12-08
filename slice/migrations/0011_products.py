# Generated by Django 4.2.4 on 2023-09-09 01:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('slice', '0010_alter_cart_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academy_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='slice.academy_product')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='slice.cart')),
                ('cart_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='slice.cartitem')),
                ('coffee_delivery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='slice.coffee_delivery')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_academy_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='slice.user_academy_product')),
                ('user_coffee_delivery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='slice.user_coffee_delivery')),
            ],
        ),
    ]

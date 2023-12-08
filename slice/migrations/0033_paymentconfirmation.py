# Generated by Django 4.2.4 on 2023-09-19 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slice', '0032_alter_usercourse_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slice.userinformation')),
            ],
        ),
    ]

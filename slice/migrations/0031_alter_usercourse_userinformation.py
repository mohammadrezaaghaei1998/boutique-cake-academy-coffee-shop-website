# Generated by Django 4.2.4 on 2023-09-18 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slice', '0030_usercourse_userinformation_alter_usercourse_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourse',
            name='userinformation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='slice.userinformation'),
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-03 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slice', '0002_remove_userinformation_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254),
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-05 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('slice', '0005_secondcontactsubmission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('price', models.FloatField(max_length=50)),
                ('hour', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='course_images/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('duration_minutes', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='slice.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
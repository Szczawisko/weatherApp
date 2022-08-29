# Generated by Django 4.0.6 on 2022-08-29 19:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_weather'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.6 on 2022-08-29 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_alter_weather_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, verbose_name='date published'),
        ),
    ]
# Generated by Django 2.0.7 on 2018-07-16 09:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20180716_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

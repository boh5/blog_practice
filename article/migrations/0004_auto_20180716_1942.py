# Generated by Django 2.0.7 on 2018-07-16 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20180716_1711'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlepost',
            options={'ordering': ('-update_time',)},
        ),
    ]

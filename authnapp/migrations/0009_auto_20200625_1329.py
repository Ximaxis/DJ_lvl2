# Generated by Django 2.2.12 on 2020-06-25 09:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authnapp', '0008_auto_20200612_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 27, 9, 29, 57, 870649, tzinfo=utc), verbose_name='актуальность ключа'),
        ),
    ]
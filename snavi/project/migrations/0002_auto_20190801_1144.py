# Generated by Django 2.2.3 on 2019-08-01 08:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateField(default=datetime.date(2019, 8, 1), verbose_name='creation date'),
        ),
    ]
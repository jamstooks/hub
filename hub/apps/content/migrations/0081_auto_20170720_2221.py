# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-20 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0080_auto_20160924_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='url',
            field=models.URLField(max_length=500),
        ),
    ]

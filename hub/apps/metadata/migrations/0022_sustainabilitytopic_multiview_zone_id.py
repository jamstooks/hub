# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-19 00:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0021_sustainabilitytopic_scpd_rss_feed'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='multiview_zone_id',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
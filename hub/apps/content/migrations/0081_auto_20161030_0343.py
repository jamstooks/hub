# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-30 03:43
from __future__ import unicode_literals

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0080_auto_20160920_1712'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contenttype',
            options={'verbose_name': 'Generic Content Type', 'verbose_name_plural': '- All Content Types -'},
        ),
        migrations.AddField(
            model_name='contenttype',
            name='authors_search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='files_search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='images_search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='websites_search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
    ]
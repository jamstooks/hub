# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-01-03 17:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0083_auto_20180313_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='GreenFund',
            fields=[
                ('contenttype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.ContentType')),
            ],
            options={
                'verbose_name': 'Green Fund',
                'verbose_name_plural': 'Green Funds',
            },
            bases=('content.contenttype',),
        ),
        migrations.AlterModelOptions(
            name='website',
            options={'ordering': ('-modified',)},
        ),
        migrations.AlterField(
            model_name='greenpowerproject',
            name='ownership_type',
            field=models.CharField(choices=[(b'unknown', b'Unknown'), (b'institution-owned', b'Institution Owned'), (b'third-party-lease', b'Third-party owned (lease)'), (b'third-party-purchase', b'Third-party owned (power purchase agreement)'), (b'other', b'Other')], max_length=200),
        ),
        migrations.AlterField(
            model_name='greenpowerproject',
            name='project_size',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='greenpowerproject',
            name='starting_ppa_price',
            field=models.CharField(blank=True, choices=[(b'< 3', b'<$0.03'), (b'4 - 4.9', b'$0.04-0.049'), (b'5 - 5.9', b'$0.05-0.059'), (b'6 - 6.9', b'$0.06-0.069'), (b'7 - 7.9', b'$0.07-0.079'), (b'8 - 8.9', b'$0.08-0.089'), (b'9 - 9.9', b'$0.09-0.099'), (b'10 - 10.9', b'$0.10-$0.109'), (b'11 - 11.9', b'$0.11-$0.119'), (b'> 12', b'>$0.12')], max_length=50, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0057_auto_20160324_0509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicprogram',
            name='completion',
            field=models.CharField(help_text=b'(e.g., "2.5 years" or "12 months")', max_length=128, null=True, verbose_name=b'Expected completion time', blank=True),
        ),
    ]

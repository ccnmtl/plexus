# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20141219_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alias',
            name='status',
            field=models.CharField(default='active', max_length=256, choices=[(b'active', b'active'), (b'pending', b'pending'), (b'deprecated', b'deprecated')]),
        ),
    ]

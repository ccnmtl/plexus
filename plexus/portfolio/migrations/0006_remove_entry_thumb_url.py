# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-04 13:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_entry_thumb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='thumb_url',
        ),
    ]

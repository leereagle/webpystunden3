# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-19 08:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stunden', '0007_auto_20161220_1710'),
    ]

    operations = [
        migrations.RenameField(
            model_name='einstellungen',
            old_name='mwst',
            new_name='ust',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stunden', '0002_firma_stundensatz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firma',
            name='stundensatz',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

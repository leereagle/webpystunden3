# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stunden', '0003_auto_20161219_0755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rechungsnummer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rechungsnummer', models.CharField(blank=True, max_length=200)),
                ('rechungsnummer_datum', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Rechungsnummer',
                'verbose_name_plural': 'Rechungsnummern',
            },
        ),
    ]
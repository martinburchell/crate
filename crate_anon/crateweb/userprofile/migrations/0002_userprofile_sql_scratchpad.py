# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-21 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='sql_scratchpad',
            field=models.TextField(default='', verbose_name='SQL scratchpad for query builder'),  # noqa
            preserve_default=False,
        ),
    ]

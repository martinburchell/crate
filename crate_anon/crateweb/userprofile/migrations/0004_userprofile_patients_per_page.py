#!/usr/bin/env python

"""
crate_anon/crateweb/userprofile/migrations/0004_userprofile_patients_per_page.py

===============================================================================

    Copyright (C) 2015-2020 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

**Userprofile app, migration 0004.**

"""
# Generated by Django 1.9.8 on 2017-02-06 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20160628_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='patients_per_page',
            field=models.PositiveSmallIntegerField(choices=[(1, '1'), (5, '5'), (10, '10'), (20, '20'), (50, '50'), (100, '100')], default=1, verbose_name='Number of patients to show per page (for Patient Explorer view)'),  # noqa
        ),
    ]

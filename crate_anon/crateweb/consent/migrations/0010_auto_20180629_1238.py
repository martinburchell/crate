#!/usr/bin/env python

"""
crate_anon/crateweb/consent/migrations/0010_auto_20180629_1238.py

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

**Consent app, migration 0010.**

"""

# Generated by Django 2.0.6 on 2018-06-29 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0009_auto_20180629_1132'),
    ]

    operations = [
        # ConsentMode
        migrations.AddField(
            model_name='consentmode',
            name='needs_processing',
            field=models.BooleanField(default=False),  # thus protecting old data from reprocessing  # noqa
        ),
        migrations.AddField(
            model_name='consentmode',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='consentmode',
            name='processed_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='consentmode',
            name='skip_letter_to_patient',
            field=models.BooleanField(default=False),
        ),
    ]

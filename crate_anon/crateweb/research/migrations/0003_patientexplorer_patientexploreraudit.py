#!/usr/bin/env python

"""
crate_anon/crateweb/research/migrations/0003_patientexplorer_patientexploreraudit.py

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

**Research app, migration 0003.**

"""
# Generated by Django 1.9.8 on 2017-02-06 16:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
# noinspection PyPackageRequirements
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('research', '0002_auto_20170203_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientExplorer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('patient_multiquery', picklefield.fields.PickledObjectField(editable=False, null=True, verbose_name='Pickled PatientMultiQuery')),  # noqa
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False, verbose_name="Deleted from the user's perspective. Audited queries are never properly deleted.")),  # noqa
                ('audited', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),  # noqa
            ],
        ),
        migrations.CreateModel(
            name='PatientExplorerAudit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('count_only', models.BooleanField(default=False)),
                ('n_records', models.IntegerField(default=0)),
                ('failed', models.BooleanField(default=False)),
                ('fail_msg', models.TextField()),
                ('patient_explorer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='research.PatientExplorer')),  # noqa
            ],
        ),
    ]

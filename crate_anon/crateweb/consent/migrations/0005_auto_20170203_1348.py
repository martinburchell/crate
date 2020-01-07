#!/usr/bin/env python

"""
crate_anon/crateweb/consent/migrations/0005_auto_20170203_1348.py

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

**Consent app, migration 0005.**

"""
# Generated by Django 1.10.5 on 2017-02-03 13:48
from __future__ import unicode_literals

from cardinal_pythonlib.django.fields.restrictedcontentfile import ContentTypeRestrictedFileField  # noqa
import crate_anon.crateweb.consent.models
import crate_anon.crateweb.consent.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0004_auto_20160703_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailattachment',
            name='file',
            field=models.FileField(storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate_filestorage'), upload_to=''),  # noqa
        ),
        migrations.AlterField(
            model_name='leaflet',
            name='pdf',
            field=ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.leaflet_upload_to),  # noqa
        ),
        migrations.AlterField(
            model_name='letter',
            name='pdf',
            field=models.FileField(storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate_filestorage'), upload_to=''),  # noqa
        ),
        migrations.AlterField(
            model_name='study',
            name='study_details_pdf',
            field=ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.study_details_upload_to),  # noqa
        ),
        migrations.AlterField(
            model_name='study',
            name='subject_form_template_pdf',
            field=ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.study_form_upload_to),  # noqa
        ),
    ]

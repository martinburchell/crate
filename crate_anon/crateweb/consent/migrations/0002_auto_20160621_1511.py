# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-21 15:11
from __future__ import unicode_literals

import crate_anon.crateweb.consent.models
import crate_anon.crateweb.consent.storage
import crate_anon.crateweb.extra.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailattachment',
            name='file',
            field=models.FileField(storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='/home/rudolf/Documents/code/crate/working/crateweb/crate_filestorage'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='leaflet',
            name='pdf',
            field=crate_anon.crateweb.extra.fields.ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='/home/rudolf/Documents/code/crate/working/crateweb/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.leaflet_upload_to),
        ),
        migrations.AlterField(
            model_name='letter',
            name='pdf',
            field=models.FileField(storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='/home/rudolf/Documents/code/crate/working/crateweb/crate_filestorage'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='study',
            name='study_details_pdf',
            field=crate_anon.crateweb.extra.fields.ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='/home/rudolf/Documents/code/crate/working/crateweb/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.study_details_upload_to),
        ),
        migrations.AlterField(
            model_name='study',
            name='subject_form_template_pdf',
            field=crate_anon.crateweb.extra.fields.ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='/home/rudolf/Documents/code/crate/working/crateweb/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.study_form_upload_to),
        ),
    ]

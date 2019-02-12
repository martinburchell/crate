# Generated by Django 2.1.5 on 2019-02-12 11:18

import cardinal_pythonlib.django.fields.restrictedcontentfile
import crate_anon.crateweb.consent.models
import crate_anon.crateweb.consent.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0015_auto_20190104_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailattachment',
            name='file',
            field=models.FileField(storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate/crate_filestorage'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='leaflet',
            name='pdf',
            field=cardinal_pythonlib.django.fields.restrictedcontentfile.ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.leaflet_upload_to),
        ),
        migrations.AlterField(
            model_name='letter',
            name='pdf',
            field=models.FileField(storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate/crate_filestorage'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='study',
            name='study_details_pdf',
            field=cardinal_pythonlib.django.fields.restrictedcontentfile.ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.study_details_upload_to),
        ),
        migrations.AlterField(
            model_name='study',
            name='subject_form_template_pdf',
            field=cardinal_pythonlib.django.fields.restrictedcontentfile.ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.study_form_upload_to),
        ),
    ]

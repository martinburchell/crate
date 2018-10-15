#!/usr/bin/env python
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

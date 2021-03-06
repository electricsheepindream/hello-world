# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-01 15:07
from __future__ import unicode_literals

from django.db import migrations, models
import music.models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_song'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.FileField(upload_to=music.models.upload_loc),
        ),
        migrations.AlterField(
            model_name='song',
            name='song',
            field=models.FileField(upload_to=music.models.upload_loc),
        ),
    ]

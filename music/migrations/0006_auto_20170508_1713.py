# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-08 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_album_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=30, verbose_name='Album_title'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-02 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_auto_20170501_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='artist',
            field=models.CharField(default='unknown', max_length=20),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-29 13:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcomments',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='subcomments',
            name='user',
        ),
        migrations.DeleteModel(
            name='SubComments',
        ),
    ]

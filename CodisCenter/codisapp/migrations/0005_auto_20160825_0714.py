# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-25 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codisapp', '0004_publicprefix'),
    ]

    operations = [
        migrations.AddField(
            model_name='codisinfo',
            name='ProjectName',
            field=models.CharField(default=11, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codisinfo',
            name='RdOwner',
            field=models.CharField(default=22, max_length=128),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-05 06:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codisapp', '0005_auto_20160825_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='codisinfo',
            name='Domain',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codisinfo',
            name='XyVIP',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codisinfo',
            name='YzVIP',
            field=models.CharField(default=22, max_length=128),
            preserve_default=False,
        ),
    ]

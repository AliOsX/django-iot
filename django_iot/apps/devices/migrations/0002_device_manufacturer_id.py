# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-05 23:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='manufacturer_id',
            field=models.CharField(default=0, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
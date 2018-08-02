# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-22 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('damage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='damage',
            name='com',
        ),
        migrations.AddField(
            model_name='damage',
            name='damageaddress',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='damage',
            name='damagearea',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='damage',
            name='damagecom',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='damage',
            name='damagetown',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='damage',
            name='damagezipcode',
            field=models.CharField(default='', max_length=6),
        ),
    ]

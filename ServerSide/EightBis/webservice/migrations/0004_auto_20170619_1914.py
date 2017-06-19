# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0003_vote_dish'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='recipe',
            field=models.CharField(max_length=20000, null=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='short_desc',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_time',
            field=models.DateField(auto_now=True),
        ),
    ]
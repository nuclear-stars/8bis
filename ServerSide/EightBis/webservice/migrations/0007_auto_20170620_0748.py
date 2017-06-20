# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0006_dailydish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailydish',
            name='extra_recipe',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_selection',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_time',
            field=models.DateField(),
        ),
    ]

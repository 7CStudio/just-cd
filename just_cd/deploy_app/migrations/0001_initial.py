# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-24 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuildInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curr_build_info', models.TextField()),
            ],
        ),
    ]
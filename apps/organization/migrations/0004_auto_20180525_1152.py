# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-05-25 11:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20180524_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='course_nums',
            new_name='courses_num',
        ),
    ]

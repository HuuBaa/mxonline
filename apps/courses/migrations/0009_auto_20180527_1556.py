# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-05-27 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='', max_length=300, verbose_name='\u8001\u5e08\u544a\u8bc9\u4f60'),
        ),
        migrations.AddField(
            model_name='course',
            name='you_need_know',
            field=models.CharField(default='', max_length=300, verbose_name='\u8bfe\u7a0b\u9700\u77e5'),
        ),
    ]

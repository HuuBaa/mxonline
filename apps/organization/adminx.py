#!/usr/bin/env python
# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/5/19 17:11'

import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'city', 'image', 'address', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'city__name', 'image', 'address', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'city__name', 'image', 'address', 'fav_nums', 'click_nums', 'add_time']

    relfield_style='fk-ajax'


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position', 'fav_nums', 'points', 'click_nums',
                    'add_time']
    search_fields = ['name', 'org__name', 'work_years', 'work_company', 'work_position', 'fav_nums', 'points', 'click_nums']
    list_filter = ['name', 'org__name', 'work_years', 'work_company', 'work_position', 'fav_nums', 'points', 'click_nums',
                   'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

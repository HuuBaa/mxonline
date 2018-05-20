#!/usr/bin/env python
# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/5/19 18:10'
import xadmin

from .models import UserAsk, UserMessage, UserCourse, UserFavorite, CourseComments


class UserAskAdmin(object):
    list_display = ['course_name', 'name', 'mobile', 'add_time']
    search_fields = ['course_name', 'name', 'mobile']
    list_filter = ['course_name', 'name', 'mobile', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ['comments', 'user', 'course', 'add_time']
    search_fields = ['comments', 'user__username', 'course__name']
    list_filter = ['comments', 'user__username', 'course__name', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user__username', 'fav_id', 'fav_type']
    list_filter = ['user__username', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user__username', 'course__name']
    list_filter = ['user__username', 'course__name', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)

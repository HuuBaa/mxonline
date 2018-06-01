#!/usr/bin/env python
# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/5/19 16:08'

import xadmin

from .models import Course, CourseResource, Video, Lesson,BannerCourse
from operation.models import CourseOrg
class LessonInline(object):
    model=Lesson
    extra=0

class CourseResourceInline(object):
    model=CourseResource
    extra=0

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time','get_course_lesson_num','go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    ordering=['-click_nums']
    readonly_fields=['fav_nums']
    list_editable=['degree','desc']
    exclude=['click_nums']
    inlines=[LessonInline,CourseResourceInline]
    refresh_times=[3,5]

    def queryset(self):
        qs=super(CourseAdmin,self).queryset()
        return qs.filter(is_banner=False)

    def save_models(self):
        #保存课程时统计课程机构的课程数
        obj=self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org=obj.course_org
            course_org.courses_num=Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    ordering=['-click_nums']
    readonly_fields=['fav_nums']
    exclude=['click_nums']
    inlines=[LessonInline,CourseResourceInline]

    def queryset(self):
        qs=super(BannerCourseAdmin,self).queryset()
        return qs.filter(is_banner=True)


class LessonAdmin(object):
    list_display = ['name','course',  'add_time']
    search_fields = ['course__name', 'name']
    list_filter = ['course__name', 'name', 'add_time']  # 外键的name字段用于筛选


class VideoAdmin(object):
    list_display = ['name','lesson','add_time']
    search_fields = ['lesson__name', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['name','course',  'download', 'add_time']
    search_fields = ['course__name', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']

xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

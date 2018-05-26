# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/5/26 16:10'

from django.conf.urls import url,include
from  .views import CourseListView

urlpatterns = [
#机构列表页
    url(r'^list/$',CourseListView.as_view(),name="course_list"),

]
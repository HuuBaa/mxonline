# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course

# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_courses=Course.objects.order_by("-add_time").all()

        hot_courses=Course.objects.order_by("-click_nums").all()[:3]

        # 课程排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        all_courses = p.page(page)


        return render(request,"course-list.html",{
            "all_courses":all_courses,
            "hot_courses":hot_courses,
            "sort":sort
        })

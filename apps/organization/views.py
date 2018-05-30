# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import  HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict,Teacher
from courses.models import Course
from operation.models import UserFavorite

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserAskForm

# Create your views here.

class OrgView(View):
    '''
    机构列表页
    '''

    def get(self, request):
        #课程
        all_orgs = CourseOrg.objects.all()
        hot_orgs= all_orgs.order_by("-click_nums")[:3]

        keywords = request.GET.get("keywords", "")
        if keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        #城市
        all_citys = CityDict.objects.all()



        #取出筛选城市
        city_id=request.GET.get("city","")
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))

        #类别筛选
        category=request.GET.get("ct","")
        if category:
            all_orgs=all_orgs.filter(category=category)

        #排序
        sort=request.GET.get("sort","")
        if sort:
            if sort=="students":
                all_orgs=all_orgs.order_by("-students")
            elif sort=="courses":
                all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5,request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort
        })

class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    def post(self,request):
        userask_form=UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask=userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}',content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type="application/json")


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self,request,org_id):
        course_org=CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums+=1
        course_org.save()
        has_fav=False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav=True
        all_courses=course_org.course_set.all()[:3]
        all_teacher=course_org.teacher_set.all()[:2]

        return  render(request,"org-detail-homepage.html",
                       {
                           "all_courses":all_courses,
                           "all_teacher":all_teacher,
                           "course_org":course_org,
                           "current_page":"home",
                           "has_fav":has_fav
                       })


class OrgCourseView(View):
    '''
    机构课程列表页
    '''

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()
        return render(request, "org-detail-course.html",
                      {
                          "all_courses": all_courses,
                          "course_org": course_org,
                          "current_page": "course",
                          "has_fav": has_fav
                      })

class OrgDescView(View):
    '''
    机构介绍页
    '''

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, "org-detail-desc.html",
                      {
                          "course_org": course_org,
                          "current_page": "desc",
                          "has_fav": has_fav
                      })

class OrgTeacherView(View):
    '''
    讲师列表页
    '''

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teacher = course_org.teacher_set.all()

        return render(request, "org-detail-teachers.html",
                      {
                          "all_teacher": all_teacher,
                          "course_org": course_org,
                          "current_page": "teacher",
                          "has_fav": has_fav
                      })


class AddFavView(View):
    '''
    用户收藏，取消收藏
    '''
    def post(self,request):
        fav_id=request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type="application/json")

        exist_records=UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            #记录已经存在，表示取消收藏
            exist_records.delete()

            if int(fav_type)==1:
                course=Course.objects.get(id=int(fav_id))
                course.fav_nums-=1
                if course.fav_nums<0: course.fav_nums=0
                course.save()
            elif int(fav_type)==2:
                org=CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums-=1
                if org.fav_nums < 0: org.fav_nums = 0
                org.save()
            elif int(fav_type) == 3:
                teacher=Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums-=1
                if teacher.fav_nums < 0: teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success","msg":"收藏"}', content_type="application/json")
        else:
            user_fav=UserFavorite()
            if int(fav_id)>0 and int(fav_type):
                user_fav.fav_id=int(fav_id)
                user_fav.fav_type=fav_type
                user_fav.user=request.user
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail","msg":"收藏错误"}', content_type="application/json")

class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self,request):
        all_teachers=Teacher.objects.all()

        keywords = request.GET.get("keywords", "")
        if keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=keywords) |
                Q(work_company__icontains=keywords) |
                Q(work_position__icontains=keywords))

        # 排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teachers=Teacher.objects.all().order_by("-click_nums")[:3]

        # 对机构讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)

        return render(request,"teachers-list.html",{
            "all_teachers":teachers,
            "sorted_teachers":sorted_teachers,
            "sort":sort
        })

class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher=Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums+=1
        teacher.save()
        all_coureses=teacher.course_set.all()
        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        has_fav_teacher = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True

        return  render(request,"teacher-detail.html",{
            "teacher":teacher,
            "sorted_teachers": sorted_teachers,
            "all_coureses":all_coureses,
            "has_fav_teacher":has_fav_teacher,
            "has_fav_org":has_fav_org
            })
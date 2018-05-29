# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite,CourseComments,UserCourse

from .models import Course,CourseResource
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_courses=Course.objects.order_by("-add_time").all()

        hot_courses=Course.objects.order_by("-click_nums").all()[:3]

        keywords=request.GET.get("keywords", "")
        if keywords:
            all_courses=all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))


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

class CourseDetailView(View):
    '''
    课程详情页
    '''
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))
        #增加课程点击数
        course.click_nums+=1
        course.save()

        #课程、机构是否收藏
        has_fav_org=False
        has_fav_course=False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
                has_fav_org=True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course=True

        #相关课程推荐
        tag=course.tag
        relate_courses=[]
        if tag:
            relate_courses=Course.objects.filter(tag=tag)[:1]

        return render(request,"course-detail.html",{
            "course":course,
            "relate_courses":relate_courses,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org
        })


class CourseInfoView(LoginRequiredMixin,View):
    '''
    课程章节信息
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        course.students+=1
        course.save()

        #查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course=UserCourse(user=request.user,course=course)
            user_course.save()


        #查找学过该课程的学生，还学过什么课程
        user_courses=UserCourse.objects.filter(course=course)
        user_ids=[user_course.user.id for user_course in user_courses] #学过该课程的所有用户的id
        all_user_course=UserCourse.objects.filter(user_id__in=user_ids)

        course_ids=[user_course.course.id for user_course in all_user_course] #学过该课程的所有用户 学过的其他课程的id
        relate_courses=Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources=CourseResource.objects.filter(course=course).all()

        return render(request, "course-video.html", {
            "course": course,
            "course_resource":all_resources,
            "relate_courses":relate_courses
        })


class CourseCommentView(LoginRequiredMixin,View):

    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 查找学过该课程的学生，还学过什么课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]  # 学过该课程的所有用户的id
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)

        course_ids = [user_course.course.id for user_course in all_user_course]  # 学过该课程的所有用户 学过的其他课程的id
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        all_comments=course.coursecomments_set.all()
        return render(request, "course-comment.html", {
            "course": course,
            "course_resource": all_resources,
            "all_comments":all_comments,
            "relate_courses":relate_courses
        })


class AddCommentView(View):
    '''
    用户添加课程评论
    '''
    def post(self,request):

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type="application/json")

        course_id=request.POST.get("course_id",0)
        comments=request.POST.get("comments","")
        if course_id>0 and comments:
            course_comment=CourseComments()
            course=Course.objects.get(id=int(course_id))

            course_comment.user=request.user
            course_comment.course=course
            course_comment.comments=comments
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type="application/json")



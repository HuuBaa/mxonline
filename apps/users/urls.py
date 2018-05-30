# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/5/30 10:23'

from django.conf.urls import url,include
from .views import UserInfoView,UploadImageView,UpdatePwdView,SendemailCodeView,UpdateEmailView,MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,MyMessageView


urlpatterns=[
    url(r'^info/$',UserInfoView.as_view(),name='info'),
    #用户头像上传
    url(r'^image/upload/$',UploadImageView.as_view(),name='image_upload'),
    #用户修改密码
    url(r'^update/pwd/$',UpdatePwdView.as_view(),name='update_pwd'),
    #邮箱验证码
    url(r'^sendemail_code/$',SendemailCodeView.as_view(),name='sendemail_code'),

    #修改邮箱
    url(r'^update_email/$',UpdateEmailView.as_view(),name='update_email'),
    #我的课程
    url(r'^mycourse/$',MyCourseView.as_view(),name='mycourse'),

    #我收藏的课程机构
    url(r'^myfav/org/$',MyFavOrgView.as_view(),name='myfav_org'),
    #我收藏的授课教师
    url(r'^myfav/teacher/$',MyFavTeacherView.as_view(),name='myfav_teacher'),
    #我收藏的课程机构
    url(r'^myfav/course/$',MyFavCourseView.as_view(),name='myfav_course'),
    #我的消息
    url(r'^mymessage/$',MyMessageView.as_view(),name='my_message'),
]
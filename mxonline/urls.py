# _*_ coding: utf-8 _*_
"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve
from django.views.generic import TemplateView

from mxonline.settings import MEDIA_ROOT
import xadmin

from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,LogoutView,IndexView
from organization.views import OrgView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$',LoginView.as_view(),name="login"),
    url(r'^logout/$',LogoutView.as_view(),name="logout"),
    url(r'^register/$',RegisterView.as_view(),name="register"),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name="active"),
    url(r'^forget/$',ForgetPwdView.as_view(),name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name="reset_pwd"),
    url(r'^modify_pwd/$',ModifyPwdView.as_view(),name="modify_pwd"),

    #课程机构url配置
    url(r'^org/', include('organization.urls',namespace="org")),

    #课程相关url配置
    url(r'^course/', include('courses.urls',namespace="course")),

    #用户中心相关url配置
    url(r'^users/', include('users.urls',namespace="users")),

    #media文件
    url(r'^media/(?P<path>.*)$', serve,{"document_root":MEDIA_ROOT}),
    #static文件
    #url(r'^static/(?P<path>.*)$', serve,{"document_root":STATIC_ROOT})
]

handler404='users.views.page_not_found'
handler500='users.views.page_error'
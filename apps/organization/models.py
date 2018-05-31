# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.

class CityDict(models.Model):
    '''
    城市
    '''
    name = models.CharField(max_length=50, verbose_name=u"城市")
    desc = models.CharField(max_length=200,verbose_name=u"城市描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"城市"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return '城市：{0}'.format(self.name)


class CourseOrg(models.Model):
    '''
    课程机构
    '''

    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    tag = models.CharField(max_length=10, verbose_name=u"机构标签", default=u"全国知名")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category=models.CharField(max_length=20,choices=(("pxjg",u"培训机构"),("gr",u"个人"),("gx",u"高校")),verbose_name=u"机构类别",default="pxjg")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
    address=models.CharField(max_length=150, verbose_name=u"机构地址")
    city=models.ForeignKey(CityDict,verbose_name=u"所在城市")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    courses_num=models.IntegerField(default=0, verbose_name=u"课程数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"课程机构"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return '教育机构：{0}'.format(self.name)


class Teacher(models.Model):
    '''
    教师
    '''
    org=models.ForeignKey(CourseOrg,verbose_name=u"所属机构")
    name = models.CharField(max_length=50, verbose_name=u"教师名称")
    age = models.IntegerField(default=18, verbose_name=u"年龄")
    work_years=models.IntegerField(default=0,verbose_name=u"工作年限")
    work_company=models.CharField(max_length=50,verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
    points=models.CharField(max_length=50, verbose_name=u"教学特点")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name=u"老师头像", max_length=100,default='')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '教师：{0}'.format(self.name)
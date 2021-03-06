# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/5/20 16:28'

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from mxonline.settings import EMAIL_FROM

import random


def generate_random_str(randomlength=8):
    str=''
    chars='QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm0123456789'
    length=len(chars)-1
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str


def send_register_email(email,send_type="register"):
    email_record=EmailVerifyRecord()
    code = generate_random_str(16)
    if send_type=="update_email":
        code=generate_random_str(4)

    email_record.code=code
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    email_title=""
    email_body=""

    if send_type=="register":
        email_title="慕学在线网注册激活链接"
        email_body="请点击下面的链接你的账号：http://127.0.0.1:8000/active/{0}/".format(code)

        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    if send_type=="forget":
        email_title="慕学在线网重置密码链接"
        email_body="请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}/".format(code)

        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    if send_type=="update_email":
        email_title="慕学在线网邮箱修改验证码"
        email_body="你的邮箱验证码为：{0}".format(code)

        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
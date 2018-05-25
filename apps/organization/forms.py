# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/5/25 9:24'

import re
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ["name", "mobile", "course_name"]

    def clean_mobile(self):
        '''
        验证手机是否合法

        '''
        mobile=self.cleaned_data['mobile']
        REGEX_MOBILE=r"^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$"
        p=re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法",code="mobile_invalid")
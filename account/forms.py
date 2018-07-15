"""

@Author  : dilless
@Time    : 2018/7/12 22:14
@File    : forms.py
"""
from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput

from account.models import UserProfile, UserInfo


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('确认密码不匹配!')
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'birth')

        # 修改templates中label的显示名称
        labels = {
            'phone': '电话',
            'birth': '生日',
        }


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('school', 'company', 'profession', 'address', 'about_me', 'photo')

        labels = {
            'school': '毕业院校',
            'company': '工作单位',
            'profession': '职业',
            'address': '地址',
            'about_me': '个人介绍',
            'photo': '头像',
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

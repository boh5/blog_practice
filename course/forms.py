"""

@Author  : dilless
@Time    : 2018/7/19 18:58
@File    : forms.py
"""
from django import forms

from course.models import Course, Lesson


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'overview')

        labels = {
            'title': '标题',
            'overview': '概览',
        }


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'video', 'description', 'attach']

        labels = {
            'course': '课程',
            'title': '标题',
            'video': '视频地址',
            'description': '视频描述',
            'attach': '附件',
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=user)

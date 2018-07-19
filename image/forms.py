"""

@Author  : dilless
@Time    : 2018/7/18 19:15
@File    : forms.py
"""
from urllib import request

from django import forms
from django.core.files.base import ContentFile
from slugify import slugify

from image.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        labels = {
            'title': '标题',
            'url': '链接地址',
            'description': '描述',
        }

    # clean_<fieldname>方法用于处理<filedname>字段
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given url does not match valid image extension.')
        return url

    def save(self, commit=True, force_insert=False, force_update=False):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{0}.{1}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image

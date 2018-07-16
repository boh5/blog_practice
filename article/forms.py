"""

@Author  : dilless
@Time    : 2018/7/16 1:20
@File    : forms.py
"""
from django import forms

from article.models import ArticleColumn, ArticlePost


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ('column',)


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title', 'body')

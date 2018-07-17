"""

@Author  : dilless
@Time    : 2018/7/16 1:20
@File    : forms.py
"""
from django import forms

from article.models import ArticleColumn, ArticlePost, Comment, ArticleTag


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ('column',)


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title', 'body')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commentator', 'body')

        labels = {
            'commentator': '昵称',
            'body': '内容',
        }


class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ('tag',)
        labels = {
            'tag': '标签',
        }
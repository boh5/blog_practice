"""

@Author  : dilless
@Time    : 2018/7/12 1:21
@File    : urls.py
"""
from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_title, name='blog_title'),
    path('<int:blog_id>/', views.blog_article, name='blog_article')
]
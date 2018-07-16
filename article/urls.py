"""

@Author  : dilless
@Time    : 2018/7/16 1:25
@File    : urls.py
"""
from django.urls import path

from article import views

app_name = 'article'

urlpatterns = [
    path('article-column/', views.article_column, name='article_column'),
    path('rename-article-column/', views.rename_article_column, name='rename_article_column'),
    path('del_article_column/', views.del_article_column, name='del_article_column'),
    path('article-post/', views.article_post, name='article_post'),
    path('article-list/', views.article_list, name='article_list'),
    path('article-detail/<int:id>/<slug:slug>/', views.article_detail, name='article_detail'),
    path('del-article/', views.del_article, name='del_article'),
    path('edit-article/<int:article_id>/', views.edit_article, name='edit-article'),
    path('list-article-titles/', views.list_article_titles, name='list_article_titles'),
    path('list-article-detail/<int:article_id>/<slug:slug>/', views.list_article_detail, name='list_article_detail'),
]

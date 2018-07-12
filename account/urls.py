"""

@Author  : dilless
@Time    : 2018/7/12 22:12
@File    : urls.py
"""
from django.urls import path
from django.contrib.auth import views as auth_views

from account import views

app_name = 'account'

urlpatterns = [
    # path('login/', views.user_login, name='user_login'),
    path('login/', auth_views.login, {'template_name': 'account/login.html'}, name='user_login'),
    path('logout/', auth_views.logout, {'template_name': 'account/logout.html'}, name='user_logout'),
    path('register/', views.register, name='user_register'),
]
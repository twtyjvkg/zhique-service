#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf.urls import url

from .views import UserRegisterAPIView, UserProfileAPIView, LoginAPIView

app_name = 'zhique_auth'

urlpatterns = [
    url(r'login', LoginAPIView.as_view(), name='login'),
    url(r'register', UserRegisterAPIView.as_view(), name='register'),
    url(r'currentUser', UserProfileAPIView.as_view()),
]
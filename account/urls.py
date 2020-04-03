#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf.urls import url

from .views import UserProfileAPIView

app_name = 'account'

urlpatterns = [

    url(r'^users/self$', UserProfileAPIView.as_view()),
]
#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf.urls import url

from .views import WebHooksAPIView

app_name = 'blog'

urlpatterns = [
    url(r'^webhook$', WebHooksAPIView.as_view()),
]


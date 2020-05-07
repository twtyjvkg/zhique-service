#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import WebHooksAPIView
from .viewsets import ArticleViewSet

app_name = 'blog'

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)

urlpatterns = [
] + router.urls


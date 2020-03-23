#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from rest_framework.routers import DefaultRouter

from .viewsets import OAuthAppViewSet

blog_router = DefaultRouter(trailing_slash=False)
blog_router.register(r'apps', OAuthAppViewSet)

app_name = 'oauth'

urlpatterns = [

] + blog_router.urls


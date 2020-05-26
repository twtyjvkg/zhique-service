#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import ActiveGlobalConfigAPIView
from .viewsets import GlobalConfigViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'global-config', GlobalConfigViewSet)

app_name = 'customize'

urlpatterns = [
url(r'^global-config/active$', ActiveGlobalConfigAPIView.as_view()),
              ] + router.urls


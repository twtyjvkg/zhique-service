#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import DocHookAPIView
from .viewsets import DocViewSet, BookViewSet

app_name = 'yuque'

router = DefaultRouter(trailing_slash=False)

router.register('docs', DocViewSet)
router.register('books', BookViewSet)

urlpatterns = [
                  url(r'^docs/hook$', DocHookAPIView.as_view()),
              ] + router.urls


#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import UserRegisterAPIView
from .viewsets import OAuthClientViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'clients', OAuthClientViewSet)

app_name = 'oauth'

urlpatterns = [
                  url(r'^register$', UserRegisterAPIView.as_view(), name='register'),
              ] + router.urls


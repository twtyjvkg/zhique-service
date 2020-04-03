#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import CallbackAPIView, LoginAPIView, UserRegisterAPIView
from .viewsets import OAuthClientViewSet

blog_router = DefaultRouter(trailing_slash=False)
blog_router.register(r'clients', OAuthClientViewSet)

app_name = 'oauth'

urlpatterns = [
                  url(r'^register$', UserRegisterAPIView.as_view(), name='register'),
                  # url(r'^(?P<oauth_type>[a-z]+)/authorize$', AuthorizeAPIView.as_view(), name='authorize'),
                  url(r'^(?P<oauth_type>[a-z]+)/callback$', CallbackAPIView.as_view(), name='callback'),
              ] + blog_router.urls


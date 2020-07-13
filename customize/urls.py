#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import ActiveSiteProfileAPIView
from .viewsets import SiteProfileViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'site-profile', SiteProfileViewSet)

app_name = 'customize'

urlpatterns = [
                  url(r'^site-profile/active$', ActiveSiteProfileAPIView.as_view()),
              ] + router.urls

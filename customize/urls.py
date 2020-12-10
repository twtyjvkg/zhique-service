#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import ActiveSiteProfileAPIView
from .viewsets import SiteProfileViewSet, CarouselViewSet, SocialAccountViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'site-profiles', SiteProfileViewSet)
router.register(r'carousels', CarouselViewSet)
router.register(r'social-accounts', SocialAccountViewSet)

app_name = 'customize'

urlpatterns = [
                  url(r'^site-profiles/active$', ActiveSiteProfileAPIView.as_view()),
              ] + router.urls


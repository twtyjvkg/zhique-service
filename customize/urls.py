#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from rest_framework.routers import DefaultRouter

from .viewsets import CarouselViewSet, SocialAccountViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'carousels', CarouselViewSet)
router.register(r'social-accounts', SocialAccountViewSet)

app_name = 'customize'

urlpatterns = [
              ] + router.urls


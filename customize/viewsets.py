#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from ZhiQue import mixins, permissions
from ZhiQue.mixins import ViewSetMixin
from .models import Card, SiteProfile, Carousel, SocialAccount
from .serializers import SiteProfileSerializer, CarouselSerializer, SocialAccountSerializer


class CardViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """卡片"""
    queryset = Card.objects.all()


class SiteProfileViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """网站配置文件"""
    queryset = SiteProfile.objects.all()
    serializer_class = SiteProfileSerializer


class CarouselViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """轮播图"""
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class SocialAccountViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """社交账号"""
    queryset = SocialAccount.objects.all()
    serializer_class = SocialAccountSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

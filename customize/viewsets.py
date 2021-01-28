#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from ZhiQue import mixins, permissions
from ZhiQue.mixins import ViewSetMixin
from .models import Card, Carousel, SocialAccount
from .serializers import CarouselSerializer, SocialAccountSerializer


class CardViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """卡片"""
    queryset = Card.objects.all()


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

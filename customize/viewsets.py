#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from ZhiQue import mixins
from ZhiQue.mixins import ViewSetMixin
from .models import Card, SiteProfile
from .serializers import SiteProfileSerializer


class CardViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """卡片"""
    queryset = Card.objects.all()


class SiteProfileViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """网站配置文件"""
    queryset = SiteProfile.objects.all()
    serializer_class = SiteProfileSerializer
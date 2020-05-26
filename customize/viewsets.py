#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from ZhiQue import mixins
from ZhiQue.mixins import ViewSetMixin
from .models import Card, GlobalConfig
from .serializers import GlobalConfigSerializer


class CardViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """卡片"""
    queryset = Card.objects.all()


class GlobalConfigViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """卡片"""
    queryset = GlobalConfig.objects.all()
    serializer_class = GlobalConfigSerializer
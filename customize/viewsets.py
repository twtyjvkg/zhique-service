#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from rest_framework import viewsets

from ZhiQue import mixins, permissions
from ZhiQue.mixins import ViewSetMixin
from .models import Card


class CardViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """卡片"""
    queryset = Card.objects.all()
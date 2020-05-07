#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'


from ZhiQue import mixins
from ZhiQue.mixins import ViewSetMixin
from .models import OAuthClient
from .serializers import OAuthClientSerializer


class OAuthClientViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, ViewSetMixin):
    """oauth应用视图集"""
    queryset = OAuthClient.objects.all()
    serializer_class = OAuthClientSerializer

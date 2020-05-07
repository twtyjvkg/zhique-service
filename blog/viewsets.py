#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from rest_framework import permissions

from ZhiQue import mixins
from ZhiQue.permissions import IsAdminUser
from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ViewSetMixin):
    """oauth应用视图集"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        action = self.action
        if action in ('create', 'delete', 'update', 'partial_update'):
            return [IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]


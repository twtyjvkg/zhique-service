#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = 'mixin'
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.db import models
from rest_framework import viewsets, mixins as _mixins, status
from rest_framework.response import Response


class BaseModelMixin(models.Model):
    """抽象model基类
    定义model的公共字段
    """
    is_active = models.BooleanField('有效', default=True, help_text='以反选代替删除。')

    class Meta:
        abstract = True


class ViewSetMixin(viewsets.GenericViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).all()


class CreateModelMixin(_mixins.CreateModelMixin):
    """创建model实例"""
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DestroyModelMixin(_mixins.DestroyModelMixin):
    """销毁model实例"""
    pass


class UpdateModelMixin(_mixins.UpdateModelMixin):
    """更新model实例"""
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RetrieveModelMixin(_mixins.RetrieveModelMixin):
    """检索model实例"""
    pass


class ListModelMixin(_mixins.ListModelMixin):
    pass

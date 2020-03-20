#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = 'mixin'
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.db import models
from rest_framework import viewsets, mixins as _mixins


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
    pass


class DestroyModelMixin(_mixins.DestroyModelMixin):
    """销毁model实例"""
    pass


class UpdateModelMixin(_mixins.UpdateModelMixin):
    """更新model实例"""
    pass


class RetrieveModelMixin(_mixins.RetrieveModelMixin):
    """检索model实例"""
    pass


class ListModelMixin(_mixins.ListModelMixin):
    pass

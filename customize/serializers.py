#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from rest_framework import serializers

from .models import SiteProfile


class SiteProfileSerializer(serializers.ModelSerializer):
    """网站配置文件序列化"""
    class Meta:
        model = SiteProfile
        fields = '__all__'
        read_only_fields = ('is_active',)


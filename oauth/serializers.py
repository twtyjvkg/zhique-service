#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from rest_framework import serializers

from .models import OAuthApp


class OAuthAppSerializer(serializers.ModelSerializer):
    """oauth应用序列化"""
    class Meta:
        model = OAuthApp
        fields = '__all__'
        read_only_fields = ('is_active',)
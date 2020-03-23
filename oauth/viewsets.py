#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from rest_framework import viewsets, status
from rest_framework.response import Response

from ZhiQue import mixins, permissions
from .models import OAuthApp
from .serializers import OAuthAppSerializer


class OAuthAppViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """oauth应用视图集"""
    queryset = OAuthApp.objects.all()
    serializer_class = OAuthAppSerializer

    def get_permissions(self):
        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
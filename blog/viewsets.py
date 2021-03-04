#!/usr/bin/python
# -*- coding: utf-8 -*-
import uuid

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response

from ZhiQue import permissions
from ZhiQue import mixins
from .filters import CategoryFilter, ArticleFilter
from .serializers import CategorySerializer, ArticleListSerializer, ArticleDetailSerializer, \
    TagSerializer, CategoryDetailSerializer
from .models import Category, Article, Tag


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_class = CategoryFilter

    def get_serializer_class(self):
        action = self.action
        if action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer


class TagViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = TagSerializer


class ArticleViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    filter_class = ArticleFilter

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        action = self.action
        if action in ('create', 'retrieve', 'update', 'partial_update'):
            return ArticleDetailSerializer
        return ArticleListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.viewed()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class HotArticleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Article.objects.filter(views__gt=0).order_by('-views')[:5]
    serializer_class = ArticleListSerializer
    permission_classes = (permissions.AllowAny,)


class RecommendArticleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Article.objects.filter(is_recommend=True)[:5]
    serializer_class = ArticleListSerializer
    permission_classes = (permissions.AllowAny,)
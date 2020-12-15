#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter

from .viewsets import ArticleViewSet, CategoryViewSet, HotArticleViewSet, TagViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'hot-articles', HotArticleViewSet)

app_name = 'blog'

urlpatterns = [] + router.urls

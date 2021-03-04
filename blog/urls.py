#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import CategoryBreadcrumbView
from .viewsets import ArticleViewSet, CategoryViewSet, HotArticleViewSet, TagViewSet, RecommendArticleViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'hot-articles', HotArticleViewSet)
router.register(r'recommend-articles', RecommendArticleViewSet)

app_name = 'blog'

urlpatterns = [
                  url(r'^category-breadcrumb$', CategoryBreadcrumbView.as_view())
              ] + router.urls


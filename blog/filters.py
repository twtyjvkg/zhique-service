#!/usr/bin/python
# -*- coding: utf-8 -*-
import django_filters

from .models import Category, Article


class CategoryFilter(django_filters.rest_framework.FilterSet):
    level = django_filters.NumberFilter(method='category_level_filter')
    parent_category = django_filters.UUIDFilter(lookup_expr='exact')

    @staticmethod
    def category_level_filter(queryset, name, value):
        id_list = []
        for category in queryset:
            if category.get_category_level() == value:
                id_list.append(category.id)
        return queryset.filter(id__in=id_list).all()

    class Meta:
        model = Category
        fields = ('level', 'parent_category')


class ArticleFilter(django_filters.rest_framework.FilterSet):
    category = django_filters.UUIDFilter(method='category_filter')

    @staticmethod
    def category_filter(queryset, name, value):
        id_list = []
        for article in queryset:
            category_tree = list(map(lambda t: t.id, article.category.get_category_tree()))
            if value in category_tree:
                id_list.append(article.id)
        return queryset.filter(id__in=id_list).all()

    class Meta:
        model = Article
        fields = ('category',)


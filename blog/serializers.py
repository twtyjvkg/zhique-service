#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from django.utils.safestring import mark_safe
from rest_framework import serializers

from .relations import ArticleCategoryField
from .utils import truncate_content
from .models import Category, Article, Tag


class CategorySerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField(read_only=True)
    path = serializers.SerializerMethodField(read_only=True)
    level = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_path(obj):
        return obj.get_category_path()

    @staticmethod
    def get_children(obj):
        queryset = Category.objects.filter(parent_category_id=obj.id)
        serializer = CategorySerializer(queryset, many=True, read_only=True)
        return serializer.data

    @staticmethod
    def get_level(obj):
        return obj.get_category_level()

    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField(read_only=True)
    level = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_parent(obj):
        if obj.parent_category is None:
            return None
        serializer = CategoryDetailSerializer(obj.parent_category, read_only=True)
        return serializer.data

    @staticmethod
    def get_level(obj):
        return obj.get_category_level()

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class ArticleSerializer(serializers.ModelSerializer):
    category = ArticleCategoryField(read_only=True)
    body = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_body(obj):
        reg = re.compile('<[^>]*>')
        return truncate_content(mark_safe(reg.sub('', obj.body)), length=100)

    @staticmethod
    def get_url(obj):
        return obj.get_absolute_url()

    class Meta:
        model = Article
        fields = '__all__'


class ArticleDetailSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(write_only=True)
    category = ArticleCategoryField(read_only=True)
    breadcrumb = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_breadcrumb(obj):
        tree = obj.get_category_tree()
        tree.append({'name': '断线的风筝', 'url': '/'})
        return tree[::-1]

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('views', 'created_time')


class HotArticleSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_url(obj):
        return obj.get_absolute_url()

    class Meta:
        model = Article
        fields = ('id', 'title', 'url', 'views')

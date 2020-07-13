#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from ZhiQue import mixins
from ZhiQue.mixins import ViewSetMixin
from .models import Doc, Book
from .serializers import DocSerializer, BookSerializer


class DocViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ViewSetMixin):
    """语雀文章"""
    queryset = Doc.objects.all()
    serializer_class = DocSerializer


class BookViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ViewSetMixin):
    """语雀文章"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
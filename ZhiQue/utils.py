#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from urllib.parse import urlparse

from django.contrib.sites.models import Site
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = "page"
    page_size = 10
    max_page_size = 100


def get_redirect_uri(request):
    redirect_uri = request.GET.get('redirect_uri', None)
    if not redirect_uri:
        redirect_uri = '/'
        return redirect_uri
    # p = urlparse(redirect_uri)
    # if p.netloc:
    #     site = Site.objects.get_current().domain
    #     if not p.netloc.replace('www.', '') == site.replace('www.', ''):
    #         return '/'
    return redirect_uri

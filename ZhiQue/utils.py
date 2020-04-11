#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import exception_handler


class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = "page"
    page_size = 10
    max_page_size = 100


def get_redirect_uri(request):
    redirect_uri = request.GET.get('redirect_uri', None)
    return redirect_uri if redirect_uri else settings.FRONT_BASE_URL


def zhique_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['errorCode'] = response.status_code
        response.data['success'] = False
        response.data['errorMessage'] = response.data['detail']
        response.data['showType'] = 1
        del response.data['detail']

    return response

#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

import json
import re

from django.utils.deprecation import MiddlewareMixin


def hump_to_underline(hump_str):
    p = re.compile(r'([a-z]|\d)([A-Z])')
    return re.sub(p, r'\1_\2', hump_str).lower()


def underline_to_hump(underline_str):
    return re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), underline_str)


def underline_dict(params):
    new_params = params
    if isinstance(params, dict):
        new_params = {}
        for k, v in params.items():
            new_params[hump_to_underline(k)] = underline_dict(params[k])
    elif isinstance(params, list):
        new_params = []
        for param in params:
            new_params.append(underline_dict(param))
    return new_params


def camel_dict(params):
    new_params = params
    if isinstance(params, dict):
        new_params = {}
        for k, v in params.items():
            new_params[underline_to_hump(k)] = camel_dict(params[k])
    elif isinstance(params, list):
        new_params = []
        for param in params:
            new_params.append(camel_dict(param))
    return new_params


class DataFormatMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        if request.method == "GET":
            request_data = underline_dict(request.GET)
            request.GET = request_data
        elif request.method == "POST" or request.method == "DELETE":
            req_body = json.loads(request.body.decode('utf-8'))
            request_data = underline_dict(req_body)
            request._body = json.dumps(request_data).encode('utf-8')
            return None

    @staticmethod
    def process_response(request, response):
        if response.status_code == 200:
            try:
                response_data = camel_dict(response.data)
                response.data = response_data
                response._is_rendered = False
                response.render()
            except Exception as e:
                print(e)
        return response


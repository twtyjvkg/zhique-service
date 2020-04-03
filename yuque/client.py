#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = '客户端'
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from urllib.parse import urlencode

import requests


class RequestError(Exception):

    def __init__(self, status_code, response_body):
        message = f'Request for yuque failed, response_code:{status_code},response_body:{response_body}'
        super().__init__(message)


class Client:
    api_host = None
    user_token = None

    def __init__(self, api_host=None, user_token=None):
        self.api_host = api_host
        self.user_token = user_token

    def request(self, api, method='GET', request_data=None, user_agent='@zhique/sdk'):
        request_url = f'{self.api_host}/{api}'
        request_header = {'User-Agent': user_agent, 'X-Auth-Token': self.user_token}
        if method == 'GET':
            func = self.get_request
        elif method == 'POST':
            func = self.post_request
        elif method == 'PUT':
            func = self.put_request
        elif method == 'DELETE':
            func = self.delete_request
        else:
            raise ValueError
        response = func(request_url, request_data, request_header)
        if response.status_code != 200:
            raise RequestError(response.status_code, response.text)
        return response.json()

    @staticmethod
    def get_request(request_url, request_data, request_header):
        if request_data:
            request_url = f'{request_url}?{urlencode(request_data)}'
        return requests.get(request_url, headers=request_header)

    @staticmethod
    def post_request(request_url, request_data, request_header=None):
        return requests.post(request_url, json=request_data, headers=request_header)

    @staticmethod
    def put_request(request_url, request_data, request_header):
        return requests.put(request_url, json=request_data, headers=request_header)

    @staticmethod
    def delete_request(request_url, request_data, request_header):
        return requests.delete(request_url, headers=request_header)
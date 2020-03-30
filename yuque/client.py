#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = '客户端'
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

import requests
from urllib.parse import urlencode

from django.shortcuts import get_object_or_404

from oauth.models import OAuthApp
from yuque.settings import *


class Client:

    def get_token(self, code):
        data = {
            'client_id': YUQUE_CLIENT_ID,
            'client_secret': YUQUE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }

        return self.request(YUQUE_TOKEN_URL, method='POST', requests_data=data)

    def get_user(self):
        return self.request(YUQUE_USER_API)

    def request(self, api, requests_data=None, method='GET'):
        request_header = {'X-Auth-Token': self.user_token} if self.user_token else {}
        if method == 'GET':
            func = self._get_request
        elif method == 'POST':
            request_header['Content-Type'] = 'application/json'
            func = self._post_request
        else:
            raise ValueError
        response = func(api, requests_data, request_header)
        if response.status_code != 200:
            pass
        return response.json()

    @staticmethod
    def _get_request(request_url, requests_data, request_header):
        if requests_data:
            request_url = f'{request_url}?{urlencode(requests_data)}'
        return requests.get(request_url, headers=request_header)

    @staticmethod
    def _post_request(request_url, requests_data, request_header):
        return requests.post(request_url, json=requests_data, headers=request_header)
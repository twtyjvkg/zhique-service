#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

import uuid
from abc import abstractmethod
from urllib.parse import urlencode

import requests
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse

from ZhiQue.utils import get_redirect_uri
from .models import OAuthClient, OAuthUser


class RequestError(Exception):
    def __init__(self, client, status_code, response_body):
        message = f'Request for {client} failed, response_code:{status_code},response_body:{response_body}'
        super().__init__(message)


class BaseOAuthClient:
    """oauth客户端基类"""
    CLIENT_TYPE = None
    client_key = None
    client_secret = None
    access_token = None
    AUTHORIZE_URL = None
    TOKEN_URL = None

    def __init__(self, access_token=None):
        self.access_token = access_token

    @property
    def is_authorized(self):
        return self.access_token is not None

    @abstractmethod
    def get_authorize_url(self, request):
        pass

    @abstractmethod
    def get_access_token_by_code(self, code):
        pass

    @abstractmethod
    def get_oauth_user_info(self):
        pass

    def request(self, request_url, method='GET', request_data=None, request_header=None, user_agent='@zhique/sdk'):
        if request_header:
            request_header['User-Agent'] = user_agent
        else:
            request_header = {'User-Agent': user_agent}
        if method == 'GET':
            func = self._get_request
        elif method == 'POST':
            func = self._post_request
        elif method == 'PUT':
            func = self._put_request
        elif method == 'DELETE':
            func = self._delete_request
        else:
            raise ValueError
        response = func(request_url, request_data, request_header)
        if response.status_code != 200:
            raise RequestError(self.CLIENT_TYPE, response.status_code, response.text)
        return response.json()

    @staticmethod
    def _get_request(request_url, request_data, request_header):
        if request_data:
            request_url = f'{request_url}?{urlencode(request_data)}'
        return requests.get(request_url, headers=request_header)

    @staticmethod
    def _post_request(request_url, request_data, request_header=None):
        return requests.post(request_url, json=request_data, headers=request_header)

    @staticmethod
    def _put_request(request_url, request_data, request_header):
        return requests.put(request_url, json=request_data, headers=request_header)

    @staticmethod
    def _delete_request(request_url, request_data, request_header):
        if request_data:
            request_url = f'{request_url}?{urlencode(request_data)}'
        return requests.delete(request_url, headers=request_header)

    def get_config(self):
        try:
            config = get_object_or_404(OAuthClient, client_type=self.CLIENT_TYPE)
            return config
        except ValueError:
            return None
        except Http404:
            return None

    class Meta:
        abstract = True


class YuQueOAuthClient(BaseOAuthClient):
    """语雀客户端"""
    CLIENT_TYPE = 'yuque'
    AUTHORIZE_URL = 'https://www.yuque.com/oauth2/authorize'
    TOKEN_URL = 'https://www.yuque.com/oauth2/token'
    API_HOST = 'https://www.yuque.com/api/v2'
    API_LIST = {
        'user': 'user'
    }

    def __init__(self, access_token=None):
        config = self.get_config()
        self.client_key = config.client_key
        self.client_secret = config.client_secret
        super(YuQueOAuthClient, self).__init__(access_token=access_token)

    def api_request(self, api, *args, **kwargs):
        request_url = f'{self.API_HOST}/{api}'
        request_header = {'X-Auth-Token': self.access_token}
        return self.request(request_url, request_header=request_header, *args, **kwargs)

    def get_authorize_url(self, request):
        state = uuid.uuid4()
        data = urlencode({
            'state': state,
            'client_id': self.client_key,
            'scope': 'group:read,repo:read,topic:read,doc:read',
            'response_type': 'code',
            'redirect_uri': reverse('authorize', request=request, kwargs={
                'authorize_type': self.CLIENT_TYPE
            })
        })
        cache.set('oauth:authorize:state:{0}'.format(state), get_redirect_uri(request), timeout=60 * 60)
        return f'{self.AUTHORIZE_URL}?{data}'

    def get_access_token_by_code(self, code):
        data = {
            'client_id': self.client_key,
            'client_secret': self.client_secret,
            'response_type': 'code',
            'code': code,
            'grant_type': 'authorization_code'
        }
        try:
            response_data = self.request(self.TOKEN_URL, method='POST', request_data=data)
            self.access_token = response_data.get('access_token')
            return self.access_token
        except RequestError:
            return None

    def get_oauth_user_info(self):
        if not self.is_authorized:
            return None
        try:
            response_data = self.api_request(self.API_LIST.get('user')).get('data')
            user, created = OAuthUser.objects.update_or_create({
                'openid': response_data.get('id'),
                'nickname': response_data.get('name'),
                'avatar': response_data.get('avatar_url'),
                'access_token': self.access_token,
                'client_type': self.CLIENT_TYPE,
            })
            return user
        except RequestError:
            return None


def get_oauth_clients():
    clients = OAuthClient.objects.filter(is_active=True).all()
    if not clients:
        return []
    client_types = [c.client_type for c in clients]
    oauth_clients = BaseOAuthClient.__subclasses__()
    return [c() for c in oauth_clients if c().CLIENT_TYPE.lower() in client_types]


def get_client_by_type(client_type):
    clients = get_oauth_clients()
    finds = list(filter(lambda c: c.CLIENT_TYPE.lower() == client_type.lower(), clients))
    if finds:
        return finds[0]
    return None

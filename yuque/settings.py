#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = '语雀配置文件'
__author__ = 'xuzhao'

from django.conf import settings

YUQUE_CLIENT_ID = getattr(settings, 'YUQUE_CLIENT_ID')
YUQUE_CLIENT_SECRET = getattr(settings, 'YUQUE_CLIENT_SECRET')
YUQUE_AUTHORIZE_URL = getattr(settings, 'YUQUE_AUTHORIZE_URL', 'https://www.yuque.com/oauth2/authorize')
YUQUE_TOKEN_URL = getattr(settings, 'YUQUE_TOKEN_URL', 'https://www.yuque.com/oauth2/token')
YUQUE_USER_API = getattr(settings, 'YUQUE_TOKEN_URL', 'https://www.yuque.com/api/v2/user')

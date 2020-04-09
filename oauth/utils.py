#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

import binascii
import os

from django.shortcuts import get_object_or_404
from .models import OAuthClient


def get_client(name=None):
    """
    获取oauth应用配置
    :param name: 应用类型
    :return: 应用信息
    """
    client = get_object_or_404(OAuthClient, name=name)
    client = {
        'id': client.id,
        'client_key': client.client_key,
        'client_secret': client.client_secret,
    }
    return client


def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()


#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.shortcuts import get_object_or_404

from .models import OAuthApp


def get_app_config(app_type=None):
    """
    获取oauth应用配置
    :param app_type: 应用类型
    :return: 应用信息
    """
    app = get_object_or_404(OAuthApp, type=app_type)
    conf = {
        'app_key': app.app_key,
        'app_secret': app.app_secret,
        'authorize_url': app.authorize_url,
        'token_url': app.token_url,
    }
    return conf


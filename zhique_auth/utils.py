#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from rest_framework.exceptions import PermissionDenied

from .serializers import UserSerializer


def jwt_response_payload_handler(login_type, user=None, request=None):
    """jwt响应处理
    序列化token的响应内容
    :param login_type: 登录类型
    :param user: 请求token的用户
    :param request: 当前请求上下文
    :return: jwt序列化结果
    """
    if not user:
        raise PermissionDenied('用户不存在')
    return {
        'user': UserSerializer(user, context={'request': request}).data,
        'current_authority': 'admin' if user.is_superuser else 'user',
        'login_type': login_type,
        'status': 'ok'
    }

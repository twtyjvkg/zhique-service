#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone
from rest_framework_jwt.authentication import JSONWebTokenAuthentication as BaseWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

User = get_user_model()

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_ip(request):
    """获取当前请求ip
    :param request: 当前请求上下文
    :return: ip地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class EmailOrUsernameModelBackend(ModelBackend):
    """自定义用户验证
    允许用户使用用户名或者邮箱登录
    允许使用密码或者邮箱验证码校验
    """

    def authenticate(self, request, username=None, password=None, login_type='account', **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username), is_active=True)
            if login_type == 'account' and user.check_password(password):
                user.last_login = timezone.now()
                user.last_login_ip = get_ip(request)
                user.save()
                return user
            else:
                # 邮箱验证码校验
                code = cache.get('account:email:{0}:login:code'.format(user.email))
                if password == code:
                    return user
                return None

        except User.DoesNotExist:
            return None


class JSONWebTokenAuthentication(BaseWebTokenAuthentication):
    pass



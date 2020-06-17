#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

LOGIN_TYPE = (
    ('account', '账户密码'),
    ('email', '邮箱验证码')
)


class UserSerializer(serializers.ModelSerializer):
    """用户模列化"""

    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ('avatar', 'last_login', 'last_login_ip', 'active')

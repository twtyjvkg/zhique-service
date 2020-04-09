#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers

from .models import OAuthClient

User = get_user_model()

LOGIN_TYPE = (
    ('account', '账户密码'),
    ('email', '邮箱验证码')
)


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化"""
    username = serializers.CharField(label='用户名', required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    code = serializers.CharField(required=True, write_only=True, max_length=6, min_length=6, label='验证码',
                                 allow_blank=False)
    email = serializers.EmailField(label='邮箱', required=True, allow_blank=False)

    @staticmethod
    def validate_email(email):
        if User.objects.filter(email=email).count() > 0:
            raise serializers.ValidationError('邮箱已注册')
        return email

    def validate_code(self, code):
        email = self.initial_data['email']
        key = 'auth:verification:code:{email}'.format(email=email)
        if cache.ttl(key) == 0:
            raise serializers.ValidationError('验证码过期')
        elif cache.get(key) != code:
            raise serializers.ValidationError('验证码错误')
        else:
            cache.delete(key)

    def validate(self, attrs):
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'email', 'password')


class OAuthClientSerializer(serializers.ModelSerializer):
    """oauth应用序列化"""
    class Meta:
        model = OAuthClient
        fields = '__all__'
        read_only_fields = ('is_active',)
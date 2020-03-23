#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.contrib.auth import get_user_model, authenticate
from django.core.cache import cache
from rest_framework import serializers
from rest_framework_jwt.compat import PasswordField, get_username_field, Serializer
from rest_framework_jwt.settings import api_settings

from .validators import UsernameValidator

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

LOGIN_TYPE = (
    ('account', '账户密码'),
    ('email', '邮箱验证码')
)


class TokenSerializer(Serializer):
    """token序列化"""

    def __init__(self, *args, **kwargs):
        """动态添加用户名和密码字段"""
        super(TokenSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(validators=[UsernameValidator()])
        self.fields['type'] = serializers.ChoiceField(choices=LOGIN_TYPE, write_only=True)
        self.fields['password'] = PasswordField(write_only=True)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password'),
            'login_type': attrs.get('type')
        }

        if all(credentials.values()):
            user = authenticate(**credentials, request=self.context['request'])

            if user:
                if not user.is_active:
                    raise serializers.ValidationError('用户不可用')

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user,
                    'login_type': attrs.get('type'),
                }
            else:
                raise serializers.ValidationError('用户名或者密码错误')
        else:
            raise serializers.ValidationError(
                '请输入"{username_field}"和密码'.format(username_field=self.username_field)
            )


class UserSerializer(serializers.ModelSerializer):
    """用户模列化"""

    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ('avatar', 'last_login', 'last_login_ip', 'active')


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

#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets


class LoginForm(AuthenticationForm):
    """登录表单"""
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={
            'id': 'username',
            'class': 'form-control',
            'aria-errormessage': 'usernameError',
            'placeholder': '用户名'
        })
        self.fields['password'].widget = widgets.PasswordInput(attrs={
            'id': 'password',
            'class': 'form-control',
            'aria-errormessage': 'passwordError',
            'placeholder': '密码'
        })


#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = '验证器'
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[a-zA-Z0-9_.]{4,16}$'
    message = '请输入4-16位字母数字以及下划线和点的组合'
    flags = 0
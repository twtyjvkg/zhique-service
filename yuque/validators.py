#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class SlugValidator(validators.RegexValidator):
    regex = r'^[a-zA-Z0-9_.]{2,36}$'
    message = '访问路径至少 2 个字符，只能输入大小写字母、横线、下划线和点'
    flags = 0

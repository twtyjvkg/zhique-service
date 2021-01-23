#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = '验证器'
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class TagColorValidator(validators.RegexValidator):
    regex = r'^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$'
    message = '请输入正确的颜色'
    flags = 0
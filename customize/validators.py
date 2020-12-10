#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = '验证器'
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class UrlOrEmailValidator:
    def __call__(self, value, *args, **kwargs):
        is_email = True
        is_url = True
        try:
            EmailValidator().__call__(value)
        except ValidationError:
            is_email = False
        try:
            URLValidator().__call__(value)
        except ValidationError:
            is_url = False
        if not is_url and not is_email:
            raise ValidationError('请输入url或者邮箱')

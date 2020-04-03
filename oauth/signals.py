#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from yuque.client import Client
from .models import OAuthUser

User = get_user_model()


@receiver(signals.post_save, sender=OAuthUser)
def create_oauth_user(sender, instance=None, created=False, **kwargs):
    oauth_type = instance.oauth_type.name
    if created:
        if oauth_type == 'yuque':
            yuque_client = Client(api_host='https://www.yuque.com/api/v2', user_token=instance.access_token)
            response_data = yuque_client.request('user')
            response_data = response_data.get('data')
            instance.nickname = response_data.get('name')
            instance.openid = response_data.get('id')
            instance.avatar = response_data.get('avatar_url')
            instance.save()
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.

from ZhiQue.mixins import BaseModelMixin


User = get_user_model()


class OAuthClient(BaseModelMixin):
    """oauth应用"""
    CLIENT_TYPE = (
        ('yuque', '语雀'),
    )
    client_type = models.CharField('类型', max_length=10, unique=True, choices=CLIENT_TYPE, default='yuque')
    client_key = models.CharField(max_length=200, verbose_name='AppKey')
    client_secret = models.CharField(max_length=200, verbose_name='AppSecret')

    def __str__(self):
        return self.get_client_type_display()

    class Meta:
        db_table = 'oauth_client'
        verbose_name = 'oauth应用'
        verbose_name_plural = verbose_name


class OAuthUser(BaseModelMixin):
    """oauth用户"""
    openid = models.CharField(max_length=50, null=True, blank=False)
    nickname = models.CharField('昵称', max_length=150, null=True, blank=True)
    avatar = models.URLField('头像', null=True, blank=True)
    access_token = models.CharField('access_token', max_length=200, null=False, blank=False)
    user = models.ForeignKey(User, verbose_name='用户', null=True, blank=True, on_delete=models.CASCADE)
    client_type = models.CharField('类型', max_length=10, unique=True, default='yuque')

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'oauth_user'
        unique_together = ('user', 'openid')
        verbose_name = 'oauth用户'
        verbose_name_plural = verbose_name
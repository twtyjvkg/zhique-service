from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from ZhiQue.mixins import BaseModelMixin

User = get_user_model()


class OAuthUser(BaseModelMixin):
    """oauth用户"""
    openid = models.CharField(max_length=50, null=False, blank=False)
    nickname = models.CharField('昵称', max_length=150, null=True, blank=True)
    avatar = models.URLField('头像', null=True, blank=True)
    access_token = models.CharField('access_token', max_length=200, null=False, blank=False)
    user = models.ForeignKey(User, verbose_name='用户', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'oauth_user'
        unique_together = ('user', 'openid')
        verbose_name = 'oauth用户'
        verbose_name_plural = verbose_name


class OAuthApp(BaseModelMixin):
    """oauth应用"""
    TYPE = (
        ('yuque', '语雀'),
    )
    type = models.CharField('类型', max_length=10, unique=True, choices=TYPE, default='yuque')
    app_key = models.CharField(max_length=200, verbose_name='AppKey')
    app_secret = models.CharField(max_length=200, verbose_name='AppSecret')
    authorize_url = models.URLField(verbose_name='认证地址', blank=False, null=False)
    token_url = models.URLField(verbose_name='token地址', blank=False, null=False)

    def __str__(self):
        return self.get_type_display()

    class Meta:
        db_table = 'oauth_app'
        verbose_name = 'oauth应用'
        verbose_name_plural = verbose_name
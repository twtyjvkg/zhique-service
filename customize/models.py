
from django.db import models
from django.core import validators

# Create your models here.
from django.utils import timezone

from ZhiQue.mixins import BaseModelMixin
from attachment.models import Attachment
from .validators import UrlOrEmailValidator


class Card(BaseModelMixin):
    """卡片"""
    code = models.CharField('卡片代码', max_length=100, unique=True, null=False, blank=False)
    name = models.CharField('卡片名称', max_length=150, null=False, blank=False)
    description = models.TextField('卡片描述')
    CARD_CATALOG = (
        ('notice', '通知类'),
    )
    catalog = models.CharField('卡片类型', choices=CARD_CATALOG, max_length=10, default='notice')

    class Meta:
        verbose_name = '卡片'
        verbose_name_plural = verbose_name

class Carousel(BaseModelMixin):
    """首页轮播"""
    link = models.URLField('推广链接', null=False, blank=False)
    attachment = models.ForeignKey(Attachment, verbose_name='附件', on_delete=models.CASCADE)
    date_from = models.DateTimeField('生效时间', default=timezone.now)
    date_to = models.DateTimeField('生效时间', null=True, blank=False)

    class Meta:
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name


class SocialAccount(BaseModelMixin):
    """社交账号"""
    title = models.CharField('标题', null=False, blank=False, max_length=50)
    icon = models.CharField('图标', null=False, blank=False, max_length=30)
    url = models.CharField('链接地址', null=True, blank=True,
                           validators=[UrlOrEmailValidator()],
                           max_length=200
                           )
    qrcode = models.ForeignKey(Attachment, verbose_name='二维码', null=True, blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'customize_social_account'
        verbose_name = '社交账号'
        verbose_name_plural = verbose_name

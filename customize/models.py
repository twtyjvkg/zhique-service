
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


class SiteProfile(BaseModelMixin):
    """网站配置文件"""
    site_name = models.CharField("网站名称", max_length=200, null=False, blank=False)
    icp_code = models.CharField('ICP备案号', max_length=50, null=True, blank=True)
    icp_url = models.URLField('ICP备案查询地址', null=True, blank=True)
    police_icp_code = models.CharField('公安备案号', max_length=50, null=True, blank=True)
    police_icp_url = models.URLField('公安备案查询地址', null=True, blank=True)

    class Meta:
        db_table = 'customize_site_profile'
        verbose_name = '网站配置文件'
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

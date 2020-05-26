from django.db import models

# Create your models here.
from ZhiQue.mixins import BaseModelMixin


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


class GlobalConfig(BaseModelMixin):
    """全局配置"""
    site_name = models.CharField("网站名称", max_length=200, null=False, blank=False)
    icp_code = models.CharField('ICP备案号', max_length=50, null=True, blank=True)
    icp_url = models.URLField('ICP备案查询地址')
    police_icp_code = models.CharField('公安备案号', max_length=50, null=True, blank=True)
    police_icp_url = models.URLField('公安备案查询地址')

    class Meta:
        db_table = 'customize_global_config'
        verbose_name = '全局配置'
        verbose_name_plural = verbose_name
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

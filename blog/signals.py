#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db.models import signals, Q
from django.dispatch import receiver
from django.utils.timezone import now

from .models import Category, Article


@receiver(signals.pre_save, sender=Category)
def pre_save_category(sender, instance=None, **kwargs):
    if instance.is_top:
        # 只允许一条记录处于置顶状态
        queryset = Category.objects.filter(~Q(id=instance.id))
        for category in queryset:
            if category.is_top:
                category.is_top = False
                category.save()


@receiver(signals.pre_save, sender=Article)
def pre_save_article(sender, instance=None, **kwargs):
    if instance.status and instance.publish_time is None:
        instance.publish_time = now()

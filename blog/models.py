from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from ZhiQue.mixins import BaseModelMixin

User = get_user_model()


class BaseModel(BaseModelMixin, models.Model):
    is_top = models.BooleanField('置顶', default=False)

    class Meta:
        abstract = True


class Article(BaseModel):
    STATUS_CHOICES = (
        (True, '草稿'),
        (False, '发表'),
    )
    title = models.CharField('标题', max_length=200, unique=True)
    body = models.TextField('正文', default=None)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

from django.db import models

# Create your models here.
from ZhiQue.mixins import BaseModelMixin
from .validators import SlugValidator


class BaseModel(BaseModelMixin, models.Model):
    is_top = models.BooleanField('置顶', default=False)
    slug = models.SlugField('路径', max_length=36, unique=True, validators=[SlugValidator()])
    created_at = models.DateTimeField('创建时间')
    updated_at = models.DateTimeField('更新时间')

    class Meta:
        abstract = True


class Book(BaseModel):
    """语雀仓库"""
    id = models.PositiveIntegerField('仓库编号', primary_key=True)
    name = models.CharField('仓库名称', max_length=50)
    description = models.TextField('介绍', default=None)

    class Meta:
        verbose_name = '仓库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Doc(BaseModel):
    """语雀文档"""
    id = models.PositiveIntegerField('文档编号', primary_key=True)
    title = models.CharField('标题', max_length=128)
    book = models.ForeignKey(Book, verbose_name='仓库信息', on_delete=models.CASCADE)
    body = models.TextField('正文 Markdown 源代码')

    class Meta:
        verbose_name = '文档'
        verbose_name_plural = verbose_name
        unique_together = ('slug', 'book')

    def __str__(self):
        return self.title

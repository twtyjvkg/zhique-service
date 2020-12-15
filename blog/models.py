from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models
import uuid

# Create your models here.
from ZhiQue.mixins import BaseModelMixin

User = get_user_model()


class BaseModel(BaseModelMixin):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    is_top = models.BooleanField('置顶', default=False)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField('名称', max_length=30, unique=True)
    parent_category = models.ForeignKey('self', verbose_name="父级分类", null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-is_top', 'name']
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_category_path(self):
        return '/blog/category/{category_id}'.format(category_id=self.id)

    def get_category_tree(self):

        category_list = []

        def parse(category):
            category_list.append(category)
            if category.parent_category:
                parse(category.parent_category)
        parse(self)
        return category_list

    def get_sub_categories(self):
        return Category.objects.filter(parent_category__id=self.id)

    def get_category_level(self):

        def parse(category, level):
            if category.parent_category is not None:
                level += 1
                parse(category.parent_category, level)
            return level

        return parse(self, 1)


class Tag(BaseModel):
    name = models.CharField('名称', unique=True, max_length=30)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['-is_top']

    def __str__(self):
        return self.name


class Article(BaseModel):
    STATUS_CHOICES = (
        (True, '草稿'),
        (False, '发表'),
    )
    title = models.CharField('标题', max_length=200, unique=True)
    body = models.TextField('正文', default=None)
    publish_time = models.DateTimeField('发表时间', null=True)
    status = models.BooleanField('文章状态', choices=STATUS_CHOICES, default=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    views = models.PositiveIntegerField('访问量', default=0)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-is_top', '-publish_time']
        get_latest_by = 'publish_time'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/blog/article/detail/{article_id}'.format(article_id=self.id)

    def get_category_tree(self):
        tree = self.category.get_category_tree()
        return list(map(lambda c: ({
            'name': c.name,
            'children': list(map(lambda m: ({
                'name': m.name,
                'url': m.get_category_path()
            }), c.get_sub_categories())),
            'url': c.get_category_path()
        }), tree))

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])
        cache.clear()
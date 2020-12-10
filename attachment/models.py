from django.db import models

# Create your models here.
from rest_framework.reverse import reverse

from ZhiQue.mixins import BaseModelMixin
import uuid


class BlobField(models.Field):
    description = 'Blob'

    def db_type(self, connection):
        return 'mediumblob'


class Attachment(BaseModelMixin):
    file_id = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField('文件名', max_length=200)
    mime_type = models.CharField('MIME类型', max_length=100)
    file_size = models.PositiveIntegerField('文件长度')
    blob = BlobField('文件内容')

    class Meta:
        verbose_name = '附件'
        verbose_name_plural = verbose_name

    def get_url(self, request):
        return reverse('attachment:download', request=request, kwargs={ 'attachment_id': self.file_id })


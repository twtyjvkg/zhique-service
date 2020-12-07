from django.core.files.base import ContentFile, File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.urls import reverse


@deconstructible
class AttachmentStorage(Storage):
    """附件存储"""

    def __init__(self, model=None):
        from .models import Attachment
        self.model = Attachment

    def _open(self, file_id, mode='rb'):
        instance = self.model.objects.get(file_id=file_id)
        file = ContentFile(instance.blob)
        file.filename = instance.file_name
        file.mimetype = instance.mime_type
        return file

    def _save(self, name, content: File):
        blob = content.read()
        mime_type = getattr(content, 'content_type', 'text/plain')
        instance = self.model.objects.create(
            file_name=name,
            blob=blob,
            file_size=content.size,
            mime_type=mime_type
        )
        return instance

    def exists(self, name):
        return self.model.objects.filter(file_name=name).exists()

attachment_storage = AttachmentStorage()

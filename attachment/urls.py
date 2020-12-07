#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path

from .views import AttachmentUploadView, AttachmentDownloadView

app_name = 'attachment'

urlpatterns = [
    url(r'upload', AttachmentUploadView.as_view(), name='upload'),
    path(r'download/<uuid:attachment_id>', AttachmentDownloadView.as_view(), name='download'),
]

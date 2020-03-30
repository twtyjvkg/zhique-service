import uuid

from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView

from ZhiQue import permissions


# class AuthorizeAPIView(GenericAPIView):
#     """语雀认证视图"""
#     permission_classes = (permissions.AllowAny,)
#
#     def get(self, *args, **kwargs):
#         try:
#             state = uuid.uuid4()
#             app =
#         except Http404:

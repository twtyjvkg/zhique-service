from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView, get_object_or_404

from ZhiQue import permissions, mixins
from .models import GlobalConfig
from .serializers import GlobalConfigSerializer


class ActiveGlobalConfigAPIView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericAPIView):
    """用户信息api视图"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = GlobalConfigSerializer

    def get_object(self):
        return get_object_or_404(GlobalConfig, is_active=True)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView, get_object_or_404

from ZhiQue import permissions, mixins
from .models import SiteProfile
from .serializers import SiteProfileSerializer


class ActiveSiteProfileAPIView(mixins.RetrieveModelMixin, GenericAPIView):
    """当前网站配置文件"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = SiteProfileSerializer

    def get_object(self):
        return get_object_or_404(SiteProfile, is_active=True)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
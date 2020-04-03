from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.generics import GenericAPIView

from ZhiQue import mixins
from .serializers import UserSerializer


class UserProfileAPIView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericAPIView):
    """用户信息api视图"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        if user.is_anonymous or not user.is_authenticated:
            return None
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


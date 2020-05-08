from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ZhiQue import permissions
from .serializers import ArticleHookSerializer


class DocHookAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ArticleHookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.get('data'))
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_200_OK)
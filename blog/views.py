from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ZhiQue import permissions
from .models import Article
from .serializers import ArticleSerializer


class WebHooksAPIView(GenericAPIView):
    """语雀webHook"""
    permission_classes = (permissions.AllowAny,)

    serializer_class = ArticleSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.get('data'))
        serializer.is_valid()
        _, created = Article.objects.update_or_create(serializer.data)
        return Response(status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
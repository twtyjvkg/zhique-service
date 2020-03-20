from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from ZhiQue import mixins
from .serializers import UserRegisterSerializer, UserSerializer, TokenSerializer

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class LoginAPIView(JSONWebTokenAPIView):
    """登录API视图"""
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            login_type = serializer.object.get('login_type')
            response_data = jwt_response_payload_handler(login_type, user, request)
            response = Response(response_data, headers={'access_token': token})
            return response

        return Response(serializer.errors, status=status.HTTP_200_OK)


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


class UserRegisterAPIView(mixins.CreateModelMixin, GenericAPIView):
    """用户注册视图"""
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
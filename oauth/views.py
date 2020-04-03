import uuid
from datetime import datetime
from urllib import parse

from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from ZhiQue import permissions, mixins
from ZhiQue.utils import get_redirect_uri
from yuque.client import Client
from .models import OAuthUser
from .serializers import TokenSerializer, UserRegisterSerializer
from .utils import get_app_config


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
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
                return response

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class AuthorizeAPIView(APIView):
    """oauth认证api视图"""
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, oauth_type=None, *args, **kwargs):
        conf = get_app_config(name=oauth_type)
        if conf:
            if oauth_type == 'yuque':
                state = uuid.uuid4()
                data = parse.urlencode({
                    'state': state,
                    'client_id': conf['app_key'],
                    'scope': 'group:read,repo:read,topic:read,doc:read',
                    'response_type': 'code',
                    'redirect_uri': reverse('oauth:callback', request=request, kwargs={
                        'oauth_type': oauth_type
                    })
                })
                next_uri = get_redirect_uri(request)
                cache.set('oauth:authorize:state:{0}'.format(state), next_uri, timeout=60 * 60)
                return HttpResponseRedirect('{0}?{1}'.format(conf['authorize_url'], data))
        raise exceptions.NotFound('认证地址错误')


class CallbackAPIView(APIView):
    """oauth认证回调视图"""
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, oauth_type=None, *args, **kwargs):
        next_uri = get_redirect_uri(request)
        access_token = None
        conf = get_app_config(name=oauth_type)
        if conf:
            if oauth_type == 'yuque':
                code = self.request.query_params['code']
                state = self.request.query_params['state']
                state_cache = 'oauth:authorize:state:{0}'.format(state)
                if cache.ttl(state_cache) == 0:
                    raise exceptions.PermissionDenied('回调接口地址错误或请求超时')
                next_uri = cache.get(state_cache)
                cache.delete(state_cache)
                yuque_client = Client()
                response_data = Client.post_request(conf['token_url'], {
                    'client_id': conf['app_key'],
                    'client_secret': conf['app_secret'],
                    'code': code,
                    'grant_type': 'authorization_code'
                })
                access_token = response_data.get('access_token')
            user = request.user
            if user.is_authenticated:
                OAuthUser.objects.update_or_create(access_token=access_token,
                                                   user=user,
                                                   oauth_type_id=conf['id']
                                                   )

        return HttpResponseRedirect(next_uri)
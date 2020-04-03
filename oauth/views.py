import uuid
from datetime import datetime
from urllib import parse

from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
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
from .forms import LoginForm
from .models import OAuthUser
from .serializers import TokenSerializer, UserRegisterSerializer
from .utils import get_app_config


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class LoginView(FormView):
    """登录视图"""
    form_class = LoginForm
    template_name = 'oauth/login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['redirect_to'] = get_redirect_uri(self.request)
        return super(LoginView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=self.request.POST, request=self.request)
        if form.is_valid():
            auth.login(self.request, form.get_user())
            return super(LoginView, self).form_valid(form)
        return self.render_to_response({
            'form': form
        })

    def get_success_url(self):
        authorize_uri = reverse('authorize')
        data = parse.urlencode({
                            'response_type': 'token',
                            'redirect_uri': get_redirect_uri(self.request)
                        })
        return f'{authorize_uri}?{data}'


class LogoutView(RedirectView):
    """退出登录"""

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return get_redirect_uri(self.request)


class AuthorizeView(RedirectView):
    """用户授权"""

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthorizeView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return get_redirect_uri(self.request)


class LoginAPIView(JSONWebTokenAPIView):
    """用户登录"""
    serializer_class = TokenSerializer

    def get(self, request, *args, **kwargs):
        pass

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
    """用户注册"""
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


# class AuthorizeAPIView(APIView):
#     """oauth认证"""
#     permission_classes = [permissions.AllowAny, ]
#
#     def get(self, request, oauth_type=None, *args, **kwargs):
#         conf = get_app_config(name=oauth_type)
#         if conf:
#             if oauth_type == 'yuque':
#                 state = uuid.uuid4()
#                 data = parse.urlencode({
#                     'state': state,
#                     'client_id': conf['app_key'],
#                     'scope': 'group:read,repo:read,topic:read,doc:read',
#                     'response_type': 'code',
#                     'redirect_uri': reverse('oauth:callback', request=request, kwargs={
#                         'oauth_type': oauth_type
#                     })
#                 })
#                 next_uri = get_redirect_uri(request)
#                 cache.set('oauth:authorize:state:{0}'.format(state), next_uri, timeout=60 * 60)
#                 return HttpResponseRedirect('{0}?{1}'.format(conf['authorize_url'], data))
#         raise exceptions.NotFound('认证地址错误')


class CallbackAPIView(APIView):
    """oauth认证回调"""
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
from urllib import parse

from django.contrib import auth
from django.contrib.auth import logout
from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from ZhiQue import permissions, mixins
from ZhiQue.utils import get_redirect_uri

from .clients import get_client_by_type
from .forms import LoginForm
from .serializers import UserRegisterSerializer
from .utils import generate_token


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
        form = LoginForm(data=self.request.POST, request=self.request)
        if form.is_valid():
            auth.login(self.request, form.get_user())
            return super(LoginView, self).form_valid(form)
        return self.render_to_response({
            'form': form
        })

    def get_success_url(self):
        authorize_uri = reverse('authorize', request=self.request,  kwargs={
            'authorize_type': 'account'
        })
        data = parse.urlencode({
            'response_type': 'token',
            'redirect_uri': get_redirect_uri(self.request)
        })
        return f'{authorize_uri}?{data}'


class OAuthLoginView(RedirectView):
    """oauth客户端登录"""

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(OAuthLoginView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, authorize_type, *args, **kwargs):
        client = get_client_by_type(authorize_type)
        return client.get_authorize_url(self.request)


class LogoutView(RedirectView):
    """退出登录"""

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_token_cache_key = f'oauth:user:id:{user.id}:token'
        if cache.ttl(user_token_cache_key):
            token = cache.get(user_token_cache_key)
            cache.delete(user_token_cache_key)
            token_user_cache_key = f'oauth:token:{token}:user:id'
            if cache.ttl(token_user_cache_key):
                cache.delete(token_user_cache_key)
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return get_redirect_uri(self.request)


class AuthorizeView(RedirectView):
    """用户授权"""

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthorizeView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, authorize_type, *args, **kwargs):
        request = self.request
        user = request.user
        token = None
        if authorize_type == 'account':
            if user.is_authenticated:
                token = generate_token()
                token_user_cache_key = f'oauth:token:{token}:user:id'
                user_token_cache_key = f'oauth:user:id:{user.id}:token'
                cache.set(token_user_cache_key, user.id, timeout=60 * 60 * 24)
                cache.set(user_token_cache_key, token)
        else:
            code = request.GET.get('code')
            client = get_client_by_type(authorize_type)
            if client.get_access_token_by_code(code):
                oauth_user = client.get_oauth_user_info()
                oauth_user.user = user
                oauth_user.save()
        if token:
            data = parse.urlencode({
                'access_token': token,
                'token_type': 'bearer'
            })
            return f'{get_redirect_uri(request)}#{data}'
        return reverse('login', request=request)


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
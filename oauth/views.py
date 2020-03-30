import uuid
from urllib import parse

from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse

from ZhiQue import permissions
from ZhiQue.utils import get_redirect_uri
from .utils import get_app_config


class AuthorizeAPIView(GenericAPIView):
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
                next_uri = get_redirect_uri(self.request)
                cache.set('oauth:authorize:state:{0}'.format(state), next_uri, timeout=60 * 60)
                return HttpResponseRedirect('{0}?{1}'.format(conf['authorize_url'], data))
        raise exceptions.NotFound('认证地址错误')


class CallbackAPIView(GenericAPIView):
    """oauth认证回调视图"""
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, oauth_type=None, *args, **kwargs):
        if oauth_type == 'yuque':
            code = self.request.query_params['code']
            state = self.request.query_params['state']
            state_cache = 'oauth:authorize:state:{0}'.format(state)
            if cache.ttl(state_cache) == 0:
                raise exceptions.PermissionDenied('回调接口地址错误或请求超时')
            next_uri = cache.get(state_cache)
            cache.delete(state_cache)
import uuid
from urllib import parse

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse

from ZhiQue import permissions
from .utils import get_app_config


class AuthorizeAPIView(GenericAPIView):
    """oauth认证api视图"""
    permission_classes = [permissions.AllowAny,]

    def get(self, request, type=None, *args, **kwargs):
        conf = get_app_config(app_type=type)
        if conf:
            if type == 'yuque':
                state = uuid.uuid4()
                data = parse.urlencode({
                    'state': state,
                    'client_id': conf['app_key'],
                    'scope': 'group:read,repo:read,topic:read,doc:read',
                    'response_type': 'code',
                    'redirect_uri': reverse('oauth:callback', request=request, kwargs={
                        'type': type
                    })
                })
                return HttpResponseRedirect('{0}?{1}'.format(conf['authorize_url'], data))


class CallbackAPIView(GenericAPIView):

    def get(self, request, type=None, *args, **kwargs):
        print(type)

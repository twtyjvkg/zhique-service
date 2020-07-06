#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import exception_handler


User = get_user_model()


class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = "page"
    page_size = 10
    max_page_size = 100


def get_redirect_uri(request):
    redirect_uri = request.GET.get('redirect_uri', None)
    from django.conf import settings
    return redirect_uri if redirect_uri else settings.FRONT_BASE_URL


def zhique_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['error_code'] = response.status_code
        response.data['success'] = False
        response.data['error_message'] = response.data['detail']
        response.data['show_type'] = 1
        del response.data['detail']

    return response


def mail_admins(subject, message, fail_silently=False, connection=None,
                html_message=None):
    """Send a message to the admins, as defined by the ADMINS setting."""
    admins = User.objects.filter(is_superuser=True, is_active=True)
    if not admins:
        return
    from django.conf import settings
    if not all(isinstance(a, (list, tuple)) and len(a) == 2 for a in settings.ADMINS):
        raise ValueError('The ADMINS setting must be a list of 2-tuples.')
    mail = EmailMultiAlternatives(
        '%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject), message,
        settings.SERVER_EMAIL,
        [a.email for a in admins],
        connection=connection
    )
    if html_message:
        mail.attach_alternative(html_message, 'text/html')
    mail.send(fail_silently=fail_silently)

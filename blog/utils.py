#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.template.defaultfilters import truncatechars_html


def truncate_content(content, length=300):
    return truncatechars_html(content, length)
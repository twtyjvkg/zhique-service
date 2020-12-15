#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.template.defaultfilters import stringfilter, truncatechars_html


@stringfilter
def truncate_content(content, length=300):
    return truncatechars_html(content, length)
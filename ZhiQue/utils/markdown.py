#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from django.utils.safestring import mark_safe
from mistune import escape, escape_link, Renderer, Markdown
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name


def block_code(text, lang, inline_styles=False, linenos=False):
    if not lang:
        text = text.strip()
        return u'<pre><code>%s</code></pre>\n' % escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter(
            noclasses=inline_styles, linenos=linenos
        )
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight">%s</div>\n' % code
        return code
    except:
        return '<pre class="%s"><code>%s</code></pre>\n' % (
            lang, escape(text)
        )


class ZhiQueMarkdownRenderer(Renderer):

    def block_code(self, text, lang=None):
        # renderer has an options
        inline_styles = self.options.get('inlinestyles')
        linenos = self.options.get('linenos')
        return block_code(text, lang, inline_styles, linenos)

    def autolink(self, link, is_email=False):
        text = link = escape(link)

        if is_email:
            link = 'mailto:%s' % link
        if not link:
            link = "#"
        nofollow = "rel='nofollow'"
        return '<a href="%s" %s>%s</a>' % (link, nofollow, text)

    def link(self, link, title, text):
        link = escape_link(link)
        nofollow = "rel='nofollow'"
        if not link:
            link = "#"
        if not title:
            return '<a href="%s" %s>%s</a>' % (link, nofollow, text)
        title = escape(title, quote=True)
        return '<a href="%s" title="%s" %s>%s</a>' % (link, title, nofollow, text)


def markdown_renderer(content):
    renderer = ZhiQueMarkdownRenderer(inlinestyles=False)

    mdp = Markdown(escape=True, renderer=renderer)
    return mark_safe(mdp(content))


def html_filter(content):
    """过滤文本中的html标签"""
    reg = re.compile('<[^>]*>')
    return mark_safe(reg.sub('', content))
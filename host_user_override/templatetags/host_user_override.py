# coding: utf-8
from __future__ import unicode_literals

import re

from django import template


register = template.Library()


def get_original_host(host):
    return re.sub(r'\d+\.user\.', '', host, 1)


@register.simple_tag(takes_context=True, name='get_original_host')
def get_original_host_tag(context):
    request = context['request']
    return get_original_host(request.get_host())


@register.simple_tag(takes_context=True)
def get_login_link(context, user):
    request = context['request']
    host = get_original_host(request.get_host())
    return 'http://{user_id}.user.{host}/'.format(host=host, user_id=user.pk)

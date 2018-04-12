# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django import template

from host_user_override import conf
from host_user_override.utils import get_original_host


register = template.Library()


@register.simple_tag(takes_context=True, name='get_original_host')
def get_original_host_tag(context):
    request = context['request']
    return get_original_host(request.get_host())


@register.simple_tag(takes_context=True)
def get_login_link(context, user):
    request = context['request']
    host = get_original_host(request.get_host())
    return conf.REDIRECT_URL_FORMAT.format(host=host, user_id=user.pk)


@register.filter()
def has_permission_to_be(user, desired_user):
    return conf.PERMISSION_CHECK(user, desired_user)

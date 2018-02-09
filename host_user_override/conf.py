# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings


prefix = 'HOSTUSEROVERRIDE_'


def get_setting(name, default=None):
    return getattr(settings, prefix+name, default)


HOST_REGEXP = get_setting('HOST_REGEXP', r'(\d+)\.user\..+')

HOST_SUB_REGEXP = get_setting('HOST_SUB_REGEXP', r'\d+\.user\.')

REDIRECT_URL_FORMAT = get_setting('REDIRECT_URL_FORMAT', 'http://{user_id}.user.{host}/')

PERMANENT_REDIRECT = get_setting('HOST_SUB_REGEXP', False)

# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings


prefix = 'HOSTUSEROVERRIDE_'


def get_setting(name, default=None):
    return getattr(settings, prefix+name, default)


def permission_check(current_user, desired_user):
    return current_user.is_superuser


HOST_REGEXP = get_setting('HOST_REGEXP', r'(\d+)\.user\..+')

HOST_SUB_REGEXP = get_setting('HOST_SUB_REGEXP', r'\d+\.user\.')

REDIRECT_URL_FORMAT = get_setting('REDIRECT_URL_FORMAT', 'http://{user_id}.user.{host}/')

PERMANENT_REDIRECT = get_setting('HOST_SUB_REGEXP', False)

PERMISSION_CHECK = get_setting('PERMISSION_CHECK', permission_check)

FORCE_ACTIVE = get_setting('FORCE_ACTIVE', False)

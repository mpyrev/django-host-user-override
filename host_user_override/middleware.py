# coding: utf-8
from __future__ import unicode_literals, absolute_import

import re
import types
from functools import wraps

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template.loader import render_to_string
from django.utils.encoding import force_text

from host_user_override import conf
from host_user_override.utils import get_original_host


_HTML_TYPES = ('text/html', 'application/xhtml+xml')

REDIRECT_RESPONSE_CLASS = HttpResponseRedirect
if conf.PERMANENT_REDIRECT:
    REDIRECT_RESPONSE_CLASS = HttpResponsePermanentRedirect


def hijack_user(user):
    old_is_active = user.is_active
    old_save = user.save
    user.is_active = True

    @wraps(old_save)
    def save(self, **kwargs):
        self.is_active = old_is_active
        old_save(**kwargs)
        self.is_active = True

    user.save = types.MethodType(save, user)


class HostUserOverrideMiddleware(object):
    """
    Overrides current user if host is like <id>.user.<host> and AuthenticationMiddleware
    tells current user is superuser.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.regexp = re.compile(conf.HOST_REGEXP)

    def get_user_id(self, host):
        match = self.regexp.match(host)
        if match is not None:
            groups = match.groups()
            if groups:
                return int(groups[0])
        return None

    def __call__(self, request):
        overridden = False
        activated = False
        original_user = request.user

        host = request.META.get('HTTP_HOST', '')
        user_id = self.get_user_id(host)

        user = request.user
        User = get_user_model()
        if user_id is not None and user_id != request.user.pk:
            try:
                user = User.objects.exclude(is_superuser=True).get(pk=user_id)
            except User.DoesNotExist:
                raise PermissionDenied

        if request.user != user and conf.PERMISSION_CHECK(request.user, user):
            request.original_user = original_user
            request.user = user
            # Force active state if setting is set
            if conf.FORCE_ACTIVE and not request.user.is_active:
                hijack_user(request.user)
                activated = True
            overridden = True
        else:
            # Redirect non-superusers to original domain
            # Probably should be 302 redirect, but we need permanent for SEO
            if user_id is not None:
                original_host = get_original_host(host)
                return REDIRECT_RESPONSE_CLASS('{scheme}://{host}{path}'.format(
                    scheme=request.scheme, host=original_host, path=request.path
                ))

        response = self.get_response(request)

        # Check for responses where the toolbar can't be inserted.
        content_encoding = response.get('Content-Encoding', '')
        content_type = response.get('Content-Type', '').split(';')[0]
        if any((getattr(response, 'streaming', False),
                'gzip' in content_encoding,
                content_type not in _HTML_TYPES)):
            return response

        if overridden:
            # Inject top banner
            content = force_text(response.content, encoding=response.charset)
            bits = re.split(r'(<body.*>)', content, flags=re.IGNORECASE)
            if len(bits) > 1:
                banner_html = render_to_string('host_user_override/banner.html', request=request, context={
                    'user': user,
                    'original': original_user,
                    'activated': activated,
                })
                bits.insert(2, banner_html)
                response.content = ''.join(bits)
                if response.get('Content-Length', None):
                    response['Content-Length'] = len(response.content)

        return response

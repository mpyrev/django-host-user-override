# coding: utf-8
from __future__ import unicode_literals

import re

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.utils.encoding import force_text


_HTML_TYPES = ('text/html', 'application/xhtml+xml')


class HostUserOverrideMiddleware(object):
    """
    Overrides current user if host is like <id>.user.<host> and AuthenticationMiddleware
    tells current user is superuser.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.regexp = re.compile(r'(\d+)\.user\..+')

    def get_user_id(self, host):
        match = self.regexp.match(host)
        if match is not None:
            groups = match.groups()
            if groups:
                return int(groups[0])
        return None

    def __call__(self, request):
        overridden = False
        original_user = request.user
        if request.user.is_superuser:
            host = request.get_host()
            user_id = self.get_user_id(host)
            if user_id is not None and user_id != request.user.pk:
                User = get_user_model()
                try:
                    user = User.objects.exclude(is_superuser=True).get(pk=user_id)
                except User.DoesNotExist:
                    raise PermissionDenied
                else:
                    overridden = True
                request.user = user

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
            insert_after = '<body>'
            pattern = re.escape(insert_after)
            bits = re.split(pattern, content, flags=re.IGNORECASE)
            if len(bits) > 1:
                bits[1] = render_to_string('host_user_override/banner.html', request=request, context={
                    'user': user,
                    'original': original_user,
                }) + bits[1]
                response.content = insert_after.join(bits)
                if response.get('Content-Length', None):
                    response['Content-Length'] = len(response.content)

        return response

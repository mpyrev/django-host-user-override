# coding: utf-8
from __future__ import unicode_literals, absolute_import

import re

from host_user_override import conf


HOST_SUB_REGEXP = re.compile(conf.HOST_SUB_REGEXP, re.UNICODE)


def get_original_host(host):
    return re.sub(HOST_SUB_REGEXP, '', host, 1)

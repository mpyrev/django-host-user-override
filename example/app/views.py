# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'app/index.html'

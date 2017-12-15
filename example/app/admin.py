# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    change_form_template = 'host_user_override/change_form.html'

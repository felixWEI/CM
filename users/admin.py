# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'is_staff')

admin.site.register(User, UserAdmin)

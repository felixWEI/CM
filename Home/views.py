# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

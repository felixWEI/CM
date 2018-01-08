# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required()
def teacher_manage(request):
    return render(request, 'teacher_manage.html')


@login_required()
def class_manage(request):
    return render(request, 'class_manage.html')


@login_required()
def arrange_class(request):
    return render(request, 'arrange_class.html')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from Info_Manage.models import TeacherInfo
# Create your views here.

import datetime


@login_required()
def teacher_manage(request):

    return render(request, 'teacher_manage.html', {'UserName': request.user.username.upper()})


@csrf_exempt
def teacher_save_and_config(request):
    teacher_table = request.POST['teacher_table'].split('&&$$')
    all_teacher = []
    for eachItem in teacher_table:
        if eachItem:
            one_teacher = eachItem.split('&&')
            if one_teacher:
                all_teacher.append(one_teacher)
    save_teacher_into_database(all_teacher)

    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def save_teacher_into_database(all_teacher):
    now = datetime.datetime.now()
    for eachItem in all_teacher:
        search_result = TeacherInfo.objects.all().filter(teacher_id=eachItem[0])
        if search_result:
            TeacherInfo.objects.filter(teacher_id=eachItem[0]).update(teacher_name=eachItem[1], first_semester=eachItem[2],
                                                                      second_semester=eachItem[3], claiming_course=eachItem[4], update_time=now)
        else:
            TeacherInfo.objects.create(teacher_id=eachItem[0], teacher_name=eachItem[1], first_semester=eachItem[2],
                                       second_semester=eachItem[3], claiming_course=eachItem[4], update_time=now)


@login_required()
def class_manage(request):
    return render(request, 'class_manage.html', {'UserName': request.user.username.upper()})


@login_required()
def arrange_class(request):
    return render(request, 'arrange_class.html', {'UserName': request.user.username.upper()})

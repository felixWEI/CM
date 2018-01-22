# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from Info_Manage.models import TeacherInfo, CourseInfo
# Create your views here.

import datetime


@login_required()
def teacher_manage(request):
    teacher_table = TeacherInfo.objects.all()
    search_result = []
    for eachItem in teacher_table:
        search_result.append([eachItem.teacher_id, eachItem.teacher_name, eachItem.first_semester, eachItem.second_semester, eachItem.claiming_course])
    summary_table = [len(search_result)]
    return render(request, 'teacher_manage.html', {'UserName': request.user.username.upper(), 'teacher_table': search_result, 'summary_table': summary_table})


@csrf_exempt
def teacher_save_and_config(request):
    teacher_table = json.loads(request.POST['teacher_table'])
    data_length = teacher_table['length']
    all_teacher = []
    for i in range(data_length):
        all_teacher.append(teacher_table[str(i)])

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
    course_table = CourseInfo.objects.all()
    search_result = []
    for eachItem in course_table:
        search_result.append([eachItem.course_id, eachItem.course_name, eachItem.course_hour,
                              eachItem.course_degree, eachItem.course_type, eachItem.class_name,
                              eachItem.course_time, eachItem.suit_teacher, eachItem.teacher_claiming,
                              eachItem.semester, eachItem.year, eachItem.update_time])
    summary_table = [len(search_result)]
    table_head = ['代码', '名称', '学位', '年级', '班级', '学期', '学时', '难度', '学生数', '教师数', '次/周', '适格教师']
    length = len(table_head)
    return render(request, 'class_manage.html', {'UserName': request.user.username.upper(), 'class_table': search_result,
                                                 'table_head': table_head, 'length': length, 'summary_table': summary_table})


@login_required()
def arrange_class(request):
    return render(request, 'arrange_class.html', {'UserName': request.user.username.upper()})

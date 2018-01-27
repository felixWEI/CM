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
        search_result.append([eachItem.course_id, eachItem.course_name, eachItem.student_type,
                              eachItem.year, eachItem.class_name, eachItem.semester,
                              eachItem.course_hour, eachItem.course_degree, eachItem.student_type,
                              eachItem.allow_teachers, eachItem.times_every_week, eachItem.suit_teacher])
    current_course_count = len(search_result)
    current_hour_count = 0
    current_degree_count = 0
    current_course_claim = 0
    for eachItem in search_result:
        current_hour_count += float(eachItem[6])
        current_degree_count += float(eachItem[7])
        if eachItem[11]:
            current_course_claim += 1
    summary_table = [current_course_count, current_hour_count, current_degree_count, current_course_claim]

    table_head = ['代码', '名称', '学位', '年级', '班级', '学期', '学时', '难度', '必/选', '教师数', '次/周', '可选教师']
    table_default = ['', '', ['本科', '法律硕士', '法学硕士', '博士'], ['17', '16', '15', '14'], '',
                     ['一', '二', '三', '四', '五', '七', '八'], '', ['1', '2', '3', '4', '5'], ['必修', '选修'], '', '']
    return render(request, 'class_manage.html', {'UserName': request.user.username.upper(), 'class_table': search_result,
                                                 'table_head': table_head, 'table_default': table_default,
                                                 'summary_table': summary_table})


@csrf_exempt
def class_save_one_row(request):
    course_info = json.loads(request.POST['row_data'])
    save_course_into_database(course_info)
    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def save_course_into_database(course_info):
    now = datetime.datetime.now()
    search_result = CourseInfo.objects.all().filter(course_id=course_info[0])
    if search_result:
        CourseInfo.objects.filter(course_id=course_info[0]).update(course_name=course_info[1], student_type=course_info[2],
                                                                    year=course_info[3], class_name=course_info[4], semester=course_info[5],
                                                                    course_hour=course_info[6], course_degree=course_info[7], course_type=course_info[8],
                                                                    allow_teachers=course_info[9], times_every_week=course_info[10], suit_teacher=course_info[11], update_time=now)
    else:
        CourseInfo.objects.create(course_id=course_info[0], course_name=course_info[1], student_type=course_info[2],
                                   year=course_info[3], class_name=course_info[4], semester=course_info[5],
                                   course_hour=course_info[6], course_degree=course_info[7], course_type=course_info[8],
                                   allow_teachers=course_info[9], times_every_week=course_info[10], suit_teacher=course_info[11], update_time=now)


@login_required()
def arrange_class(request):
    return render(request, 'arrange_class.html', {'UserName': request.user.username.upper()})

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from Info_Manage.models import TeacherInfo, CourseInfo, CurrentStepInfo
# Create your views here.

import xlrd
import datetime


@login_required()
def teacher_manage(request):
    teacher_table = TeacherInfo.objects.all()
    search_result = []
    for eachItem in teacher_table:
        search_result.append([eachItem.teacher_id, eachItem.teacher_name, eachItem.first_semester,
                              eachItem.second_semester, eachItem.first_semester_expect, eachItem.second_semester_expect])
    current_teacher_count = len(search_result)
    expect_for_semester1 = 0
    expect_for_semester2 = 0
    others_semester1 = 0
    others_semester2 = 0
    summary_table = [current_teacher_count, expect_for_semester1, expect_for_semester2, others_semester1, others_semester2]
    table_head = ['教师代码', '教师姓名', '期望学时1', '期望学时2', '估算学时1', '估算学时2']
    return render(request, 'teacher_manage.html', {'UserName': request.user.username.upper(),
                                                   'teacher_table': search_result, 'summary_table': summary_table, 'table_head': table_head})


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
def teacher_personal(request):
    course_table = CourseInfo.objects.all()
    search_result = []
    for eachItem in course_table:
        search_result.append([eachItem.course_id, eachItem.course_name, eachItem.student_type,
                              eachItem.year, eachItem.class_name, eachItem.semester,
                              eachItem.course_hour, eachItem.course_degree, eachItem.student_type,
                              eachItem.allow_teachers, eachItem.times_every_week, eachItem.suit_teacher])
    expect_semester1 = '100'
    expect_semester2 = '100'
    summary_table = [expect_semester1, expect_semester2]

    table_head = ['代码', '名称', '学位', '年级', '班级', '学期', '学时', '难度', '必/选', '教师数', '周上课次数', '可选教师']
    default_value_for_class = ['法学理论', '法律史', '宪法学', '民商法学', '诉讼法学', '经济法学', '环保法', '国际法学', '刑法学',
                               '宪法学与行政法学', '环境与资源保护法', '国际法', '二专', '法学院本科', '跨校辅修']
    table_default = ['', '', ['本科', '法律硕士', '法学硕士', '博士'], ['17', '16', '15', '14'], default_value_for_class,
                    ['一', '二', '三', '四', '五', '七', '八'], '', ['1', '2', '3', '4', '5'], ['必修', '选修'], '', '']
    return render(request, 'teacher_personal.html', {'UserName': request.user.username.upper(), 'class_table': search_result,
                                                 'table_head': table_head, 'table_default': table_default,
                                                 'summary_table': summary_table})


@csrf_exempt
def teacher_request_course(request):
    course_id = request.POST['course_id']
    save_teacher_to_course_info(course_id, request.user.username.upper())
    # TODO: result part
    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


@csrf_exempt
def teacher_table_upload(request):
    input_file = request.FILES.get("file_data", None)
    work_book = xlrd.open_workbook(filename=None, file_contents=input_file.read())
    # TODO: result part
    work_sheet = work_book.sheet_by_name('教师列表')
    line_length = work_sheet.nrows
    line_width = work_sheet.row_len(0)
    for line_number in range(line_length)
    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def save_teacher_to_course_info(course_id, user_name):
    search_result = CourseInfo.objects.all().filter(course_id=course_id)
    if search_result:
        CourseInfo.objects.filter(course_id=course_id).update(suit_teacher=user_name)
    else:
        return False


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

    table_head = ['代码', '名称', '学位', '年级', '班级', '学期', '学时', '难度', '必/选', '教师数', '周上课次数', '可选教师']
    default_value_for_class = ['法学理论', '法律史', '宪法学', '民商法学', '诉讼法学', '经济法学', '环保法', '国际法学', '刑法学',
                               '宪法学与行政法学', '环境与资源保护法', '国际法', '二专', '法学院本科', '跨校辅修']
    table_default = ['', '', ['本科', '法律硕士', '法学硕士', '博士'], ['17', '16', '15', '14'], default_value_for_class,
                     ['一', '二', '三', '四', '五', '七', '八'], ['54', '36'], ['1', '2', '3', '4', '5'], ['必修', '选修'], '', '']
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
        CourseInfo.objects.filter(course_id=course_info[0]).update(course_id=course_info[0],course_name=course_info[1], student_type=course_info[2],
                                                                    year=course_info[3], class_name=course_info[4], semester=course_info[5],
                                                                    course_hour=course_info[6], course_degree=course_info[7], course_type=course_info[8],
                                                                    allow_teachers=course_info[9], times_every_week=course_info[10], suit_teacher=course_info[11], update_time=now)
    else:
        CourseInfo.objects.create(course_id=course_info[0], course_name=course_info[1], student_type=course_info[2],
                                   year=course_info[3], class_name=course_info[4], semester=course_info[5],
                                   course_hour=course_info[6], course_degree=course_info[7], course_type=course_info[8],
                                   allow_teachers=course_info[9], times_every_week=course_info[10], suit_teacher=course_info[11], update_time=now)


@csrf_exempt
def class_delete_one_row(request):
    course_id = request.POST['course_id']
    delete_course_from_database(course_id)
    # TODO: result part
    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def delete_course_from_database(course_id):
    search_result = CourseInfo.objects.all().filter(course_id=course_id)
    if search_result:
        CourseInfo.objects.filter(course_id=course_id).delete()
    else:
        return False


@login_required()
def arrange_class(request):
    step_info = []
    step_position = ['active', 'disabled', 'disabled', 'disabled', 'disabled']
    search_result = CurrentStepInfo.objects.all()
    if len(search_result) == 1:
        if search_result[0].arrange_class_status == 'start':
            step_info.append(search_result[0].s1_year_info)
            step_position[0] = 'disabled'
            step_position[1] = 'active'
            if search_result[0].s2_undergraduate:
                step_info.append(int(search_result[0].s2_undergraduate))
            if search_result[0].s2_postgraduate_1:
                step_info.append(int(search_result[0].s2_postgraduate_1))
            if search_result[0].s2_postgraduate_2:
                step_info.append(int(search_result[0].s2_postgraduate_2))
            if search_result[0].s2_doctor:
                step_info.append(int(search_result[0].s2_doctor))
    return render(request, 'arrange_class.html', {'UserName': request.user.username.upper(), 'step_info': step_info,
                                                  'step_position': step_position})


@csrf_exempt
def arrange_step_1(request):
    year = request.POST['year']
    search_result = CurrentStepInfo.objects.all()
    if search_result:
        pass
    else:
        CurrentStepInfo.objects.create(arrange_class_status='start', s1_year_info=year, s2_undergraduate='0', s2_postgraduate_1='0',
                                       s2_postgraduate_2='0', s2_doctor='0')
    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


@csrf_exempt
def arrange_step_2(request):
    button_id = request.POST['id']
    search_result = CurrentStepInfo.objects.all()
    result = 'Pass'
    if len(search_result) == 1:
        if button_id == 's2_r1_c1':
            button_value = int(search_result[0].s2_undergraduate)
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_undergraduate=str(button_value+1))
        elif button_id == 's2_r1_c2':
            button_value = int(search_result[0].s2_postgraduate_1)
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_postgraduate_1=str(button_value+1))
        elif button_id == 's2_r1_c3':
            button_value = int(search_result[0].s2_postgraduate_2)
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_postgraduate_2=str(button_value+1))
        elif button_id == 's2_r1_c4':
            button_value = int(search_result[0].s2_doctor)
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_doctor=str(button_value+1))
        else:
            result = 'Fail'
    result = json.dumps({'result': result})
    return HttpResponse(result)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from Info_Manage.models import TeacherInfo, CourseInfo, CurrentStepInfo
# Create your views here.

import os
import sys
import xlrd
import math
from datetime import datetime
import xlwt
from io import StringIO, BytesIO
reload(sys)
sys.setdefaultencoding('utf-8')

STUDENT_TYPE = ['本科', '法学硕士', '法律硕士', '法学博士']
CLASS_NAME_LIST = ["第二专业教学", "通识教育","法学专业教育", "跨校辅修教学", "基础教育", "法律硕士(法学)", "法律硕士(非法学)1班",
                   "法律硕士(非法学)2班", "法律硕士在职生", "法律史", "法学理论", "国际法学", "环境与资源保护法学", "经济法学",
                   "民商法学", "诉讼法学", "刑法学", "宪法学与行政法学"]
CLASS_GRADE = [str(datetime.now().year - i) for i in [2000, 2001, 2002, 2003]]
SEMESTER = ['一', '二']
COURSE_HOUR = ['18', '36', '54', '56', '72']
COURSE_DEGREE = ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10']
COURSE_TYPE = ['必修', '选修']
current_school_year = '{}-{}'.format(datetime.now().year, datetime.now().year+1)


@login_required()
def teacher_manage(request):
    search_result = CurrentStepInfo.objects.all()
    if search_result:
        year = search_result[0].s1_year_info
    else:
        year = 'None'
    teacher_table = TeacherInfo.objects.all()
    course_table = CourseInfo.objects.all()
    search_result = []
    weight_total_1 = 1
    weight_total_2 = 1
    apply_done = 0
    for eachItem in teacher_table:
        weight_total_1 += eachItem.first_semester_expect
        weight_total_2 += eachItem.second_semester_expect
        if eachItem.teacher_apply_done and eachItem.teacher_apply_done == '申报结束':
            apply_done += 1
        search_result.append([eachItem.teacher_id, eachItem.teacher_name, eachItem.first_semester_expect*100,
                              eachItem.second_semester_expect*100, eachItem.first_semester_hours,
                              eachItem.second_semester_hours, eachItem.first_semester_degree,
                              eachItem.second_semester_degree, eachItem.teacher_apply_done, eachItem.notes])
    current_teacher_count = len(search_result)
    total_hours_1 = 0
    total_hours_2 = 0
    total_degree_1 = 0
    total_degree_2 = 0
    for eachItem in course_table:
        if eachItem.semester == '一':
            total_hours_1 += eachItem.course_hour
            total_degree_1 += eachItem.course_degree
        else:
            total_hours_2 += eachItem.course_hour
            total_degree_2 += eachItem.course_degree
    expect_hours_for_semester1 = math.ceil((total_hours_1/weight_total_1)/18)*18
    expect_hours_for_semester2 = math.ceil((total_hours_2/weight_total_2)/18)*18
    expect_degree_for_semester1 = round(total_degree_1/weight_total_1, 2)
    expect_degree_for_semester2 = round(total_degree_2/weight_total_2, 2)

    summary_table = [current_teacher_count, apply_done, expect_hours_for_semester1, expect_hours_for_semester2,
                     expect_degree_for_semester1, expect_degree_for_semester2]
    table_head = ['教师代码', '教师姓名', '期望学时1(%)', '期望学时2(%)', '已分配学时1', '已分配学时2','已分配难度1',
                  '已分配难度2' ,'申报完成', '特殊理由']
    return render(request, 'teacher_manage.html', {'UserName': request.user.last_name+request.user.first_name+request.user.username,
                                                   'teacher_table': search_result, 'summary_table': summary_table,
                                                   'table_head': table_head, 'year': year})


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
    now = datetime.now()
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
    search_result = TeacherInfo.objects.filter(teacher_id=request.user.username)
    status = 'free'
    if search_result:
        if search_result[0].teacher_apply_done:
            status = 'lock'
    now = datetime.now().replace()
    search_result = CurrentStepInfo.objects.all()
    if search_result and search_result[0].s2_deadline:
        delta = (search_result[0].s2_deadline.replace(tzinfo=None) - now).total_seconds()
        if delta < 0.0:
            status = 'lock'
    if search_result:
        year = search_result[0].s1_year_info
    else:
        year = 'None'
    course_table = CourseInfo.objects.all()
    search_result = []
    tmp = ''
    for eachItem in course_table:
        if request.user.last_name+request.user.first_name in eachItem.teacher_ordered.split(','):
            tmp = '已申报'
        else:
            tmp = ''

        search_result.append([eachItem.course_id, eachItem.course_name, eachItem.student_type, eachItem.class_name,
                              eachItem.semester, eachItem.course_hour, eachItem.course_degree, eachItem.course_type,
                              eachItem.allow_teachers, eachItem.times_every_week, tmp])

    search_result_teacher = TeacherInfo.objects.filter(teacher_id=request.user.username)
    if search_result_teacher:
        expect_semester1 = str(search_result_teacher[0].first_semester_expect*100)
        expect_semester2 = str(search_result_teacher[0].second_semester_expect*100)
    else:
        expect_semester1 = 0
        expect_semester2 = 0
    summary_table = [expect_semester1, expect_semester2]

    table_head = ['代码', '名称', '学位', '班级', '学期', '学时', '难度', '必/选', '教师数', '周上课次数', '课程状态']
    table_default = ['', '', STUDENT_TYPE, CLASS_NAME_LIST, ['一', '二'], COURSE_HOUR, COURSE_DEGREE, ['必修', '选修'], '', '', '']
    return render(request, 'teacher_personal.html', {'UserName': request.user.last_name+request.user.first_name+request.user.username, 'class_table': search_result,
                                                 'table_head': table_head, 'table_default': table_default,
                                                 'summary_table': summary_table, 'year': year, 'status': status})


@csrf_exempt
def teacher_request_course(request):
    course_id = request.POST['course_id']
    searchResult = TeacherInfo.objects.filter(teacher_id=request.user.username)
    if searchResult:
        teacher_name = searchResult[0].teacher_name
    else:
        teacher_name = '教务员'
    if 'status' not in request.POST.keys():
        status = save_teacher_to_course_info(course_id, teacher_name)
    else:
        status = remove_teacher_from_course_info(course_id, teacher_name)
    # TODO: result part
    result = json.dumps({'status': status})
    return HttpResponse(result)


@csrf_exempt
def teacher_change_expect(request):
    modify_0 = request.POST['modify_0']
    modify_1 = request.POST['modify_1']
    modify_0 = float(modify_0) / 100.0
    modify_1 = float(modify_1) / 100.0
    if 'teacher_id' in request.POST.keys():
        teacher_id = request.POST['teacher_id']
    else:
        teacher_id = request.user.username
    searchResult = TeacherInfo.objects.filter(teacher_id=teacher_id)
    status = '修改期望失败'
    if searchResult:
        TeacherInfo.objects.filter(teacher_id=teacher_id).update(first_semester_expect=modify_0, second_semester_expect=modify_1)
        status = 'Success'
    result = json.dumps({'status': status})
    return HttpResponse(result)


@csrf_exempt
def teacher_table_upload(request):
    input_file = request.FILES.get("file_data", None)
    work_book = xlrd.open_workbook(filename=None, file_contents=input_file.read())
    # TODO: result part
    work_sheet = work_book.sheet_by_name('教师列表')
    line_length = work_sheet.nrows
    teacher_list = []
    line_width = work_sheet.row_len(0)
    for line_number in range(line_length):
        teacher_id, teacher_name, _ = work_sheet.row(line_number)
        if type(teacher_id.value) == int or type(teacher_id.value) == float:
            teacher_list.append([int(teacher_id.value), teacher_name.value])
    insert_teacher_list_into_db(teacher_list)
    return HttpResponse('Pass')


def insert_teacher_list_into_db(teacher_list):
    for eachTeacher in teacher_list:
        searchResult = TeacherInfo.objects.all().filter(teacher_id=eachTeacher[0])
        if searchResult:
            TeacherInfo.objects.filter(teacher_id=eachTeacher[0]).update(teacher_name=eachTeacher[1])
        else:
            TeacherInfo.objects.create(teacher_id=eachTeacher[0], teacher_name=eachTeacher[1], first_semester_expect=1.0, second_semester_expect=1.0)


def save_teacher_to_course_info(course_id, user_name):
    search_result = CourseInfo.objects.all().filter(course_id=course_id)
    if search_result:
        teacher_list = search_result[0].teacher_ordered.split(',')
        if len(teacher_list) == 1 and teacher_list[0] == '':
            teacher_str = user_name
        else:
            if user_name not in teacher_list:
                teacher_list.append(user_name)
            teacher_str = ','.join(teacher_list)
        CourseInfo.objects.filter(course_id=course_id).update(teacher_ordered=teacher_str, suit_teacher=teacher_str)
    return 'Success'


def remove_teacher_from_course_info(course_id, user_name):
    search_result = CourseInfo.objects.all().filter(course_id=course_id)
    status = 'Success'
    if search_result:
        teacher_list = search_result[0].teacher_ordered.split(',')
        if len(teacher_list) == 0:
            status = '你并未申报此课程, 取消失败'
        else:
            if user_name in teacher_list:
                teacher_list.remove(user_name)
            else:
                status = '你并未申报此课程, 取消失败'
            teacher_str = ','.join(teacher_list)
        CourseInfo.objects.filter(course_id=course_id).update(teacher_ordered=teacher_str, suit_teacher=teacher_str)
    return status


@csrf_exempt
def teacher_submit_apply_status(request):
    status_code = request.POST['status']
    teacher_id = request.POST['teacher_id']
    search_result = TeacherInfo.objects.filter(teacher_id=teacher_id)
    if search_result:
        teacher_name = search_result[0].teacher_name
    else:
        result = json.dumps({'status': '该老师没有在系统中注册'})
        return HttpResponse(result)
    if status_code == 'check':
        search_result = CourseInfo.objects.all()
        result_teacher = {STUDENT_TYPE[0]: [], STUDENT_TYPE[1]: [], STUDENT_TYPE[2]: [], STUDENT_TYPE[3]: []}
        for eachCourse in search_result:
            teacher_list = eachCourse.teacher_ordered.split(',')
            if teacher_name in teacher_list:
                tmp = [eachCourse.course_id, eachCourse.course_name, eachCourse.course_degree]
                result_teacher[eachCourse.student_type].append(tmp)
        # print result_teacher
        status = 'Success'
        result = json.dumps({'status': status, 'list_1': result_teacher[STUDENT_TYPE[0]], 'list_2': result_teacher[STUDENT_TYPE[1]],
                             'list_3': result_teacher[STUDENT_TYPE[2]], 'list_4': result_teacher[STUDENT_TYPE[3]]})
    elif status_code == 'save':
        status = 'Success'
        notes = request.POST['notes']
        if notes:
            TeacherInfo.objects.filter(teacher_id=teacher_id).update(teacher_apply_done='申报结束', notes=notes)
        else:
            TeacherInfo.objects.filter(teacher_id=teacher_id).update(teacher_apply_done='申报结束')
        result = json.dumps({'status': status})
    else:
        status = 'Unknown status code {}'.format(status_code)
        result = json.dumps({'status': status})
    return HttpResponse(result)


@login_required()
def class_manage(request):
    search_result = CurrentStepInfo.objects.all()
    if search_result:
        current_year = search_result[0].s1_year_info
    else:
        current_year = 'None'
    course_table = CourseInfo.objects.all()
    search_result = []
    class_name = CLASS_NAME_LIST
    student_type = STUDENT_TYPE
    year = CLASS_GRADE
    semester = SEMESTER
    course_hour = COURSE_HOUR
    course_degree = COURSE_DEGREE
    course_type = COURSE_TYPE
    current_course_count = len(course_table)
    current_hour_count = 0
    current_degree_count = 0
    current_course_claim = 0
    for eachItem in course_table:
        if not eachItem.class_name:
            continue
        for eachClass in eachItem.class_name.split(' '):
            tmp_student = eachClass.split('-')[0]
            tmp_class_grade, tmp_class_name = eachClass.split('-')[-1].split('_')
            search_result.append([eachItem.course_id, eachItem.course_name, tmp_student,
                                  tmp_class_grade, tmp_class_name, eachItem.semester,
                                  eachItem.course_hour, eachItem.course_degree, eachItem.course_type,
                                  eachItem.allow_teachers, eachItem.times_every_week, eachItem.suit_teacher])
        current_hour_count += float(eachItem.course_hour)
        current_degree_count += float(eachItem.course_degree)
        if eachItem.suit_teacher:
            current_course_claim += 1
    summary_table = [current_course_count, current_hour_count, current_degree_count, current_course_claim]

    table_head = ['代码', '名称', '学位', '年级', '班级', '学期', '学时', '难度', '必/选', '教师数', '周上课次数', '可选教师']
    table_default = ['', '', student_type, year, class_name,
                     semester, course_hour, course_degree, course_type, '', '']
    return render(request, 'class_manage.html', {'UserName': request.user.last_name+request.user.first_name+request.user.username, 'class_table': search_result,
                                                 'table_head': table_head, 'table_default': table_default,
                                                 'summary_table': summary_table, 'year': current_year})


@csrf_exempt
def class_filter_by_submit(request):
    student_type = request.POST['type'].strip().split(' ')
    semester = request.POST['semester'].strip().split(' ')
    table_id = request.POST['table_id']
    course_table = CourseInfo.objects.all()
    search_result = []
    for eachItem in course_table:
        if eachItem.semester in semester and eachItem.student_type in student_type:
            if table_id == 'table_course_manage':
                for eachClass in eachItem.class_name.split(' '):
                    search_result.append([eachItem.course_id, eachItem.course_name, eachItem.student_type,
                                          eachClass.split('-')[-1].split('_')[0], eachClass.split('-')[-1].split('_')[-1], eachItem.semester,
                                          eachItem.course_hour, eachItem.course_degree, eachItem.course_type,
                                          eachItem.allow_teachers, eachItem.times_every_week, eachItem.suit_teacher])
            elif table_id == 'table_course_personal':
                teacher_list = eachItem.teacher_ordered.split(',') if eachItem.teacher_ordered else []
                if request.user.username in teacher_list:
                    tmp = '已申报'
                else:
                    tmp = ''
                search_result.append([eachItem.course_id, eachItem.course_name, eachItem.student_type,
                                      eachItem.class_name, eachItem.semester, eachItem.course_hour,
                                      eachItem.course_degree, eachItem.course_type,
                                      eachItem.allow_teachers, eachItem.times_every_week, tmp])
    result = json.dumps({'result': search_result})
    return HttpResponse(result)


@csrf_exempt
def class_save_one_row(request):
    course_info = json.loads(request.POST['row_data'])
    old_class_info = request.POST['old_data']
    if 'old_course_id' in request.POST:
        old_course_id = request.POST['old_course_id']
        save_course_into_database_by_edit(course_info, old_class_info, old_course_id)
    else:
        save_course_into_database_by_add(course_info, old_class_info)
    result = 'Success'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def save_course_into_database_by_edit(course_info, old_class_info, old_course_id=None):
    now = datetime.now()
    search_result = CourseInfo.objects.all().filter(course_id=course_info[0])
    if search_result:
        combine_class_name = '{}-{}_{}'.format(course_info[2], course_info[3], course_info[4])
        if combine_class_name in search_result[0].class_name:
            CourseInfo.objects.filter(id=search_result[0].id).update(course_id=course_info[0],
                                                                     course_name=course_info[1],

                                                                     semester=course_info[5],
                                                                     course_hour=course_info[6],
                                                                     course_degree=course_info[7],
                                                                     course_type=course_info[8],
                                                                     allow_teachers=course_info[9],
                                                                     times_every_week=course_info[10],
                                                                     suit_teacher=course_info[11],
                                                                     update_time=now)
        else:
            class_list = search_result[0].class_name.split(' ')
            class_list.append(combine_class_name)
            if old_class_info:
                class_list.remove(old_class_info)
                suit_teacher = course_info[11]
            else:
                suit_teacher = search_result[0].suit_teacher
            class_name_str = ' '.join(class_list)
            CourseInfo.objects.filter(id=search_result[0].id).update(course_id=course_info[0],
                                                                     course_name=course_info[1],
                                                                     class_name=class_name_str,
                                                                     semester=course_info[5],
                                                                     course_hour=course_info[6],
                                                                     course_degree=course_info[7],
                                                                     course_type=course_info[8],
                                                                     allow_teachers=course_info[9],
                                                                     times_every_week=course_info[10],
                                                                     suit_teacher=suit_teacher,
                                                                     update_time=now)
    else:
        # remove class from previous course
        search_result = CourseInfo.objects.filter(course_id=old_course_id)
        class_list = search_result[0].class_name.split(' ')
        if old_class_info not in class_list:
            return '{} not in {}'.format(old_class_info, old_course_id)
        else:
            class_list.remove(old_class_info)
            if len(class_list) == 0:
                CourseInfo.objects.filter(course_id=old_course_id).delete()
            else:
                class_name_str = ' '.join(class_list)
                CourseInfo.objects.filter(course_id=old_course_id).update(class_name=class_name_str)
        # add a new course
        combine_class_name = '{}-{}_{}'.format(course_info[2], course_info[3], course_info[4])
        CourseInfo.objects.create(course_id=course_info[0], course_name=course_info[1], student_type=course_info[2],year=current_school_year,
                                  class_name=combine_class_name, semester=course_info[5],
                                  course_hour=course_info[6], course_degree=course_info[7], course_type=course_info[8],
                                  allow_teachers=course_info[9], times_every_week=course_info[10],
                                  suit_teacher='', teacher_ordered='', update_time=now)


def save_course_into_database_by_add(course_info, old_class_info):
    now = datetime.now()
    search_result = CourseInfo.objects.all().filter(course_id=course_info[0])
    if search_result:
        combine_class_name = '{}-{}_{}'.format(course_info[2], course_info[3], course_info[4])
        if combine_class_name in search_result[0].class_name:
            CourseInfo.objects.filter(id=search_result[0].id).update(course_id=course_info[0],
                                                                     course_name=course_info[1],
                                                                     semester=course_info[5],
                                                                     course_hour=course_info[6],
                                                                     course_degree=course_info[7],
                                                                     course_type=course_info[8],
                                                                     allow_teachers=course_info[9],
                                                                     times_every_week=course_info[10],
                                                                     suit_teacher=course_info[11],
                                                                     update_time=now)
        else:
            class_list = search_result[0].class_name.split(' ')
            class_list.append(combine_class_name)
            if old_class_info:
                class_list.remove(old_class_info)
                suit_teacher = course_info[11]
            else:
                suit_teacher = search_result[0].suit_teacher
            class_name_str = ' '.join(class_list)
            CourseInfo.objects.filter(id=search_result[0].id).update(course_id=course_info[0],
                                                                     course_name=course_info[1],
                                                                     class_name=class_name_str,
                                                                     semester=course_info[5],
                                                                     course_hour=course_info[6],
                                                                     course_degree=course_info[7],
                                                                     course_type=course_info[8],
                                                                     allow_teachers=course_info[9],
                                                                     times_every_week=course_info[10],
                                                                     suit_teacher=suit_teacher,
                                                                     update_time=now)
    else:
        combine_class_name = '{}-{}_{}'.format(course_info[2], course_info[3], course_info[4])
        CourseInfo.objects.create(course_id=course_info[0], course_name=course_info[1], student_type=course_info[2], year=current_school_year,
                                  class_name=combine_class_name, semester=course_info[5],
                                  course_hour=course_info[6], course_degree=course_info[7], course_type=course_info[8],
                                  allow_teachers=course_info[9], times_every_week=course_info[10],
                                  suit_teacher='', teacher_ordered='', update_time=now)


def save_course_into_database(course_info):
    now = datetime.now()
    search_result = CourseInfo.objects.all().filter(course_id=course_info[0])
    if search_result:
        CourseInfo.objects.filter(id=search_result[0].id).update(course_id=course_info[0],course_name=course_info[1], student_type=course_info[2],
                                                                    year=current_school_year, class_name=course_info[4], semester=course_info[5],
                                                                    course_hour=course_info[6], course_degree=course_info[7], course_type=course_info[8],
                                                                    allow_teachers=course_info[9], times_every_week=course_info[10], suit_teacher=course_info[11], teacher_ordered=course_info[12],update_time=now)
    else:
        CourseInfo.objects.create(course_id=course_info[0], course_name=course_info[1], student_type=course_info[2],
                                   year=current_school_year, class_name=course_info[4], semester=course_info[5],
                                   course_hour=course_info[6], course_degree=course_info[7], course_type=course_info[8],
                                   allow_teachers=course_info[9], times_every_week=course_info[10], suit_teacher=course_info[11], teacher_ordered=course_info[12],update_time=now)


@csrf_exempt
def class_delete_one_row(request):
    course_id = request.POST['course_id']
    old_class_info = request.POST['old_data']
    delete_course_from_database(course_id, old_class_info)
    # TODO: result part
    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def delete_course_from_database(course_id, old_class_info):
    search_result = CourseInfo.objects.all().filter(course_id=course_id)
    if search_result:
        if len(search_result[0].class_name.split(' ')) > 1:
            class_list = search_result[0].class_name.split(' ')
            class_list.remove(old_class_info)
            class_name_str = ' '.join(class_list)
            CourseInfo.objects.filter(course_id=course_id).update(class_name=class_name_str)
        else:
            CourseInfo.objects.filter(course_id=course_id).delete()
    else:
        return False


@csrf_exempt
def class_get_suit_teacher(request):
    course_id = request.POST['course_id']
    search_result = CourseInfo.objects.filter(course_id=course_id)
    if search_result:
        teacher_list = search_result[0].suit_teacher.split(',')
    result_list = []
    for eachTeacher in teacher_list:
        search_result = TeacherInfo.objects.filter(teacher_name=eachTeacher)
        if search_result:
            tmp = [search_result[0].teacher_id, eachTeacher]
            result_list.append(tmp)
    result = json.dumps({'result_list': result_list})
    return HttpResponse(result)


@csrf_exempt
def class_table_upload(request):
    input_file = request.FILES.get("file_data", None)
    work_book = xlrd.open_workbook(filename=None, file_contents=input_file.read())
    # TODO: result part
    work_sheet = work_book.sheet_by_name('课程信息')
    line_length = work_sheet.nrows
    line_content = []
    for line_number in range(line_length):
        if line_number == 0:
            continue
        line_content.append(work_sheet.row(line_number))
    class_info_to_save = []
    for eachLine in line_content:

        course_id = eachLine[7].value
        course_name = eachLine[8].value
        student_type = eachLine[3].value
        year = eachLine[1].value
        class_name = '{}-{}_{}'.format(student_type, int(eachLine[4].value) if eachLine[4].value else '', eachLine[5].value)
        semester = eachLine[2].value
        course_hour = eachLine[10].value
        course_degree = eachLine[11].value
        course_type = eachLine[12].value
        allow_teachers = eachLine[14].value
        times_every_week = eachLine[16].value
        suit_teacher = eachLine[17].value
        teacher_ordered = eachLine[17].value
        class_info_to_save.append([course_id, course_name, student_type, year, class_name, semester, course_hour,
                                   course_degree, course_type, allow_teachers, times_every_week, suit_teacher, teacher_ordered])

    save_course_table_into_database(class_info_to_save)
    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def save_course_table_into_database(class_info_to_save):
    course_dict = {}
    output = ""
    for eachCourse in class_info_to_save:
        if eachCourse[0] not in course_dict.keys():
            course_dict[eachCourse[0]] = eachCourse
        else:
            if course_dict[eachCourse[0]][5] != eachCourse[5]:
                output += "{}, 学期信息与相同课程号发生冲突\n".format(eachCourse)
            elif eachCourse[4].split('_')[0] not in course_dict[eachCourse[0]][4]:
                output += "{}, 班级信息与相同课程号发生冲突\n".format(eachCourse)
            else:
                course_dict[eachCourse[0]][4] += ' {}'.format(eachCourse[4])

    for tmpKey in course_dict.keys():
        each_course = course_dict[tmpKey]
        save_course_into_database(each_course)
    return output


@csrf_exempt
def class_get_teacher_name(request):
    teacher_str = request.POST['teacher_str']
    search_result = TeacherInfo.objects.all().filter(teacher_name=teacher_str)
    status = 'Success'
    if search_result:
        teacher_name = teacher_str
        teacher_id = search_result[0].teacher_id
    else:
        search_result = TeacherInfo.objects.filter(teacher_id=teacher_str)
        if search_result:
            teacher_id = teacher_str
            teacher_name = search_result[0].teacher_name
        else:
            teacher_name = ''
            teacher_id = ''
            status = 'Fail'
    result = json.dumps({'teacher_name': teacher_name, 'teacher_id': teacher_id, 'status': status})
    return HttpResponse(result)


@csrf_exempt
def class_search_from_course_id(request):
    course_id = request.POST['course_id']
    search_result = CourseInfo.objects.filter(course_id=course_id)
    raw_data = []
    if search_result:
        class_list = search_result[0].class_name.split(' ')
        tmp_class_grade, tmp_class_name = class_list[0].split('-')[-1].split('_')
        raw_data.extend([search_result[0].course_name, search_result[0].student_type, tmp_class_grade, tmp_class_name, search_result[0].semester,
                         str(search_result[0].course_hour), str(search_result[0].course_degree), search_result[0].course_type,
                         search_result[0].allow_teachers, search_result[0].times_every_week])
    if raw_data:
        status = 'Success'
    else:
        status = 'Fail'

    result = json.dumps({'raw_data': raw_data, 'status':status})
    return HttpResponse(result)


@login_required()
def arrange_class(request):
    step_info = []
    step_position = ['active', 'disabled', 'disabled', 'disabled', 'disabled']
    search_result = CurrentStepInfo.objects.all()
    if len(search_result) == 1:
        if search_result[0].arrange_class_status == 'start':
            step_info.append(search_result[0].s1_year_info)
            step_position[1] = 'active'
            if search_result[0].s2_undergraduate:
                step_info.append(int(search_result[0].s2_undergraduate))
            if search_result[0].s2_postgraduate_1:
                step_info.append(int(search_result[0].s2_postgraduate_1))
            if search_result[0].s2_postgraduate_2:
                step_info.append(int(search_result[0].s2_postgraduate_2))
            if search_result[0].s2_doctor:
                step_info.append(int(search_result[0].s2_doctor))
            if search_result[0].s2_start_request:
                s2_start_request = int(search_result[0].s2_start_request)
                now = datetime.now().replace()
                if search_result[0].s2_deadline:
                    delta = (search_result[0].s2_deadline.replace(tzinfo=None) - now).total_seconds()
                    if delta < 0.0:
                        s2_start_request = 3
                step_info.append(s2_start_request)
            if search_result[0].s2_deadline:
                deadline_string = search_result[0].s2_deadline.strftime('%Y %m %d %H %M')
                step_info.append(deadline_string)
            if search_result[0].s2_teacher_confirm_u:
                step_info.append(int(search_result[0].s2_teacher_confirm_u))
            if search_result[0].s2_teacher_confirm_p1:
                step_info.append(int(search_result[0].s2_teacher_confirm_p1))
            if search_result[0].s2_teacher_confirm_p2:
                step_info.append(int(search_result[0].s2_teacher_confirm_p2))
            if search_result[0].s2_teacher_confirm_d:
                step_info.append(int(search_result[0].s2_teacher_confirm_d))

        if search_result[0].s3_status_flag == 'start arrange':
            step_position[2] = 'active'
        elif search_result[0].s3_status_flag == 'arrange over':
            step_position[2] = 'active'
            step_position[3] = 'active'
        else:
            pass
        if search_result[0].s4_status_flag:
            step_info.append(int(search_result[0].s4_teacher_confirm_u))
            step_info.append(int(search_result[0].s4_teacher_confirm_p1))
            step_info.append(int(search_result[0].s4_teacher_confirm_p2))
            step_info.append(int(search_result[0].s4_teacher_confirm_d))

        if search_result[0].s5_status_flag:
            if search_result[0].s5_status_flag == 'lock start':
                step_position[4] = 'active'
            elif search_result[0].s5_status_flag == 'lock done':
                step_position[0] = 'disabled'
                step_position[1] = 'disabled'
                step_position[2] = 'disabled'
                step_position[3] = 'disabled'
                step_position[4] = 'active'
                step_info.append('lock done')
            else:
                pass

    times = [[i for i in range(1, 13)], [i for i in range(1, 32)], [i for i in range(24)], [i for i in range(1, 60)]]
    return render(request, 'arrange_class.html', {'UserName': request.user.last_name+request.user.first_name+request.user.username, 'step_info': step_info,
                                                  'step_position': step_position, 'times': times})


@csrf_exempt
def arrange_step_1(request):
    year = request.POST['year']
    search_result = CurrentStepInfo.objects.all()
    if search_result:
        pass
    else:
        CurrentStepInfo.objects.create(arrange_class_status='start', s1_year_info=year, s2_undergraduate='0', s2_postgraduate_1='0',
                                       s2_postgraduate_2='0', s2_doctor='0', s2_teacher_confirm_u='0',s2_teacher_confirm_p1='0',s2_teacher_confirm_p2='0',s2_teacher_confirm_d='0')
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
        elif button_id == 's2_r2_c1':
            button_value = int(search_result[0].s2_start_request)
            deadline_string = request.POST['deadline']
            year, month, day, hour, minute = deadline_string.split(' ')
            deadline_time = datetime(int(year), int(month), int(day), int(hour), int(minute))
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_start_request='2', s2_deadline=deadline_time)
        elif button_id == 's2_r3_c1':
            button_value = int(search_result[0].s2_teacher_confirm_u)
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_teacher_confirm_u=str(button_value + 1))
        elif button_id == 's2_r3_c2':
            button_value = int(search_result[0].s2_teacher_confirm_p1)
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_teacher_confirm_p1=str(button_value + 1))
        elif button_id == 's2_r3_c3':
            button_value = int(search_result[0].s2_teacher_confirm_p2)
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_teacher_confirm_p2=str(button_value + 1))
        elif button_id == 's2_r3_c4':
            button_value = int(search_result[0].s2_teacher_confirm_d)
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_teacher_confirm_d=str(button_value + 1))
        else:
            result = 'Fail'
        tmp = CurrentStepInfo.objects.all().filter(id=search_result[0].id)
        if len(tmp) == 1 and 's2_r1' in button_id:
            if tmp[0].s2_undergraduate == '2' and tmp[0].s2_postgraduate_1 == '2' and tmp[0].s2_postgraduate_2 == '2' and tmp[0].s2_doctor == '2':
                CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_start_request='1')
                result = 'start request'
    result = json.dumps({'result': result})
    return HttpResponse(result)


@csrf_exempt
def arrange_step_3(request):
    status = request.POST['status']
    result = {}
    result['status'] = 'Pass'
    search_result = CurrentStepInfo.objects.all()
    if len(search_result) == 1:
        if status == 'start arrange':
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s3_status_flag=status)
        elif status == 'init info':
            result['info'] = start_arrange()
        elif status == 'arrange main':
            arrange_main()
        elif status == 'arrange over':
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s3_status_flag=status,
                                                                          s4_status_flag='adjustment start',
                                                                          s4_teacher_confirm_u='0',
                                                                          s4_teacher_confirm_p1='0',
                                                                          s4_teacher_confirm_p2='0',
                                                                          s4_teacher_confirm_d='0')
        else:
            result['status'] = 'Fail'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def start_arrange():
    search_result_course = CourseInfo.objects.all()
    search_result_teacher = TeacherInfo.objects.all()
    teacher_count = len(search_result_teacher)
    teacher_with_expect = []
    teacher_without_expect = []
    expect_count = 0
    total_count = 0
    for eachTeacher in search_result_teacher:
        if eachTeacher.first_semester_expect != 1.0 or eachTeacher.second_semester_expect != 1.0:
            teacher_with_expect.append(eachTeacher.teacher_id)
            expect_count += (eachTeacher.first_semester_expect + eachTeacher.second_semester_expect)
        else:
            teacher_without_expect.append(eachTeacher.teacher_id)
        total_count += (eachTeacher.first_semester_expect + eachTeacher.second_semester_expect)
    degree_count = [0]*10
    [degree_count_u, degree_count_p1, degree_count_p2, degree_count_d] = [[0]*len(COURSE_DEGREE),
                                                                          [0]*len(COURSE_DEGREE),
                                                                          [0]*len(COURSE_DEGREE),
                                                                          [0]*len(COURSE_DEGREE)]
    [hours_u, hours_p1, hours_p2, hours_d] = [[], [], [], []]
    total_hours = 0
    total_courses = len(search_result_course)
    for eachCourse in search_result_course:
        degree_count[int(eachCourse.course_degree)-1] += 1
        total_hours += eachCourse.course_hour
        if eachCourse.student_type == STUDENT_TYPE[3]:
            degree_count_d[int(eachCourse.course_degree)-1] += 1
            hours_d.append(eachCourse.course_hour)
        elif eachCourse.student_type == STUDENT_TYPE[2]:
            degree_count_p2[int(eachCourse.course_degree)-1] += 1
            hours_p2.append(eachCourse.course_hour)
        elif eachCourse.student_type == STUDENT_TYPE[1]:
            degree_count_p1[int(eachCourse.course_degree) - 1] += 1
            hours_p1.append(eachCourse.course_hour)
        elif eachCourse.student_type == STUDENT_TYPE[0]:
            degree_count_u[int(eachCourse.course_degree) - 1] += 1
            hours_u.append(eachCourse.course_hour)
        else:
            continue
    teacher_with_expect_count = len(teacher_with_expect)
    total_hours_with_expect = (expect_count/total_count)*total_hours
    teacher_without_expect_count = teacher_count - teacher_with_expect_count
    ave_hours_without_expect = (total_hours - total_hours_with_expect)/teacher_without_expect_count
    degree_count = [round(float(each)/teacher_count, 1) for each in degree_count]
    degree_count.reverse()
    degree_count_u.reverse()
    degree_count_p1.reverse()
    degree_count_p2.reverse()
    degree_count_d.reverse()
    tmp_u,tmp_p1,tmp_p2,tmp_d = [0]*len(COURSE_HOUR),[0]*len(COURSE_HOUR),[0]*len(COURSE_HOUR),[0]*len(COURSE_HOUR)
    for index, item in enumerate(COURSE_HOUR):
        tmp_d[index] = hours_d.count(int(item))
        tmp_p1[index] = hours_p1.count(int(item))
        tmp_p2[index] = hours_p2.count(int(item))
        tmp_u[index] = hours_u.count(int(item))
    degree_count_u.extend(tmp_u)
    degree_count_p1.extend(tmp_p1)
    degree_count_p2.extend(tmp_p2)
    degree_count_d.extend(tmp_d)
    return [teacher_count, teacher_with_expect_count, total_hours_with_expect, teacher_without_expect_count, round(ave_hours_without_expect, 2),
            degree_count, total_courses, [degree_count_u, degree_count_p1, degree_count_p2, degree_count_d]]


def arrange_main():
    file_obj = open('analysis_result.txt', 'w+')
    search_result_course = CourseInfo.objects.all()
    search_result_teacher = TeacherInfo.objects.all()
    teacher_1 = {}
    teacher_2 = {}
    result_1 = {}
    result_2 = []
    # 权重值
    total_weight = [0, 0]
    for eachTeacher in search_result_teacher:
        tmp_dict = {'id': eachTeacher.teacher_id, 'expect_1': eachTeacher.first_semester_expect,
                    'expect_2': eachTeacher.second_semester_expect, 'total_1': 0, 'total_2': 0}
        total_weight[0] += float(eachTeacher.first_semester_expect)
        total_weight[1] += float(eachTeacher.second_semester_expect)
        teacher_1[eachTeacher.teacher_name] = tmp_dict
        teacher_2[eachTeacher.teacher_id] = eachTeacher.teacher_name

    total_hours = [0, 0]
    total_degrees = [0, 0]
    for eachCourse in search_result_course:
        if eachCourse.semester == '一':
            total_hours[0] += eachCourse.course_hour
            total_degrees[0] += eachCourse.course_degree
        else:
            total_hours[1] += eachCourse.course_hour
            total_degrees[1] += eachCourse.course_degree
    hours_ave_1 = total_hours[0]/total_weight[0]
    hours_ave_2 = total_hours[1]/total_weight[1]
    degree_ave_1 = total_degrees[0]/total_weight[0]
    degree_ave_2 = total_degrees[1]/total_weight[1]
    # # 关于一个学分取整
    # hours_ave_1 = (hours_ave_1 / 18 + 1) * 18
    # hours_ave_2 = (hours_ave_2 / 18 + 1) * 18
    for eachTeacher in search_result_teacher:
        expect_hours_1 = math.ceil(eachTeacher.first_semester_expect * hours_ave_1 / 18) * 18
        expect_hours_2 = math.ceil(eachTeacher.first_semester_expect * hours_ave_2 / 18) * 18
        expect_degree_1 = eachTeacher.first_semester_expect * degree_ave_1
        expect_degree_2 = eachTeacher.first_semester_expect * degree_ave_2
        tmp_dict = {'course_list': [], 'degree_list': [], 'total_hours_1': 0, 'expect_hours_1': expect_hours_1, 'total_hours_2': 0,
                    'expect_hours_2': expect_hours_2, 'expect_degree_1': expect_degree_1, 'expect_degree_2': expect_degree_2,
                    'total_degree_1': 0, 'total_degree_2': 0}
        result_1[eachTeacher.teacher_id] = tmp_dict
    print >>file_obj, '<STEP 1 Limitation for teacher list>'
    for eachCourse in search_result_course:
        teacher_list = eachCourse.suit_teacher.split(',')
        if len(teacher_list) == int(eachCourse.allow_teachers):
            for eachTeacher in teacher_list:
                result_1[teacher_1[eachTeacher]['id']]['course_list'].append(eachCourse.course_id)
                result_1[teacher_1[eachTeacher]['id']]['degree_list'].append(eachCourse.course_degree)
                if eachCourse.semester == '一':
                    tmp_str1 = 'total_hours_1'
                    tmp_str2 = 'total_degree_1'
                else:
                    tmp_str1 = 'total_hours_2'
                    tmp_str2 = 'total_degree_2'
                result_1[teacher_1[eachTeacher]['id']][tmp_str1] += int(eachCourse.course_hour)
                result_1[teacher_1[eachTeacher]['id']][tmp_str2] += int(eachCourse.course_degree)
        else:
            result_2.append(eachCourse)
    show_statistical(result_1, file_obj)
    result_1, result_2 = balance_for_high_degree(result_1, result_2, teacher_1, file_obj)
    show_statistical(result_1, file_obj)
    result_1, result_2 = balance_for_course_hour(result_1, result_2, teacher_1, file_obj)
    show_statistical(result_1, file_obj)
    result_3 = {}
    for tmpKey in result_1.keys():
        for eachCourse in result_1[tmpKey]['course_list']:
            if CourseInfo.objects.get(course_id=eachCourse).semester == '一':
                TeacherInfo.objects.filter(teacher_id=tmpKey).update(first_semester_hours=result_1[tmpKey]['total_hours_1'], first_semester_degree=result_1[tmpKey]['total_degree_1'])
            else:
                TeacherInfo.objects.filter(teacher_id=tmpKey).update(second_semester_hours=result_1[tmpKey]['total_hours_2'], second_semester_degree=result_1[tmpKey]['total_degree_2'])
            if eachCourse not in result_3.keys():
                result_3[eachCourse] = [teacher_2[tmpKey]]
            else:
                result_3[eachCourse].append(teacher_2[tmpKey])
    for tmpKey in result_3.keys():
        tmp = ",".join(result_3[tmpKey])
        CourseInfo.objects.filter(course_id=tmpKey).update(teacher_auto_pick=tmp, teacher_final_pick=tmp)
    file_obj.close()
    HttpResponse('Pass')


def show_statistical(result_1, file_obj):
    print >>file_obj, '##########################################################'
    print >>file_obj, 'showing available information'
    for tmpKey in result_1.keys():
        avail_hours_1 = result_1[tmpKey]['expect_hours_1'] - result_1[tmpKey]['total_hours_1']
        avail_hours_2 = result_1[tmpKey]['expect_hours_2'] - result_1[tmpKey]['total_hours_2']
        avail_degree_1 = result_1[tmpKey]['expect_degree_1'] - result_1[tmpKey]['total_degree_1']
        avail_degree_2 = result_1[tmpKey]['expect_degree_2'] - result_1[tmpKey]['total_degree_2']
        print >>file_obj, 'teacher id: {} available hours {} {} available degree {} {}'.format(tmpKey, avail_hours_1, avail_hours_2,
                                                                                   avail_degree_1, avail_degree_2)
    print >>file_obj, '##########################################################'


# 先学时大小再老师个数
def sort_new_1(result_list):
    result_list = sorted(result_list, key=lambda x: x.course_hour, reverse=True)
    result_list_tmp = []
    key_value = []
    for eachItem in result_list:
        if eachItem.course_hour in key_value:
            result_list_tmp[key_value.index(eachItem.course_hour)].append(eachItem)
        else:
            key_value.append(eachItem.course_hour)
            result_list_tmp.append([eachItem])
    result_list = []
    for eachItem in result_list_tmp:
        if len(eachItem) > 1:
            tmp = sorted(eachItem, key=lambda x: len(x.suit_teacher.split(',')))
            result_list.extend(tmp)
        else:
            result_list.append(eachItem[0])
    # for eachItem in result_list:
    #     print eachItem.course_hour
    #     print len(eachItem.suit_teacher.split(','))
    return result_list


# 先available学时 再 available难度
def sort_new_2(result_list, result_all_teacher, key_value_1, key_value_2, key_value_3, key_value_4):
    result_list = sorted(result_list, key=lambda x: (result_all_teacher[x][key_value_1]-result_all_teacher[x][key_value_2]), reverse=True)
    result_list_tmp = []
    key_value = []
    for eachItem in result_list:
        available = result_all_teacher[eachItem][key_value_1]-result_all_teacher[eachItem][key_value_2]
        if available in key_value:
            result_list_tmp[key_value.index(available)].append(eachItem)
        else:
            result_list_tmp.append([eachItem])
            key_value.append(available)
    result_list = []
    for eachItem in result_list_tmp:
        if len(eachItem) > 1:
            tmp = sorted(eachItem, key=lambda x: (result_all_teacher[x][key_value_3]-result_all_teacher[x][key_value_4]), reverse=True)
            result_list.extend(tmp)
        else:
            result_list.append(eachItem[0])
    # for eachItem in result_list:
    #     print 'teacher id {}'.format(eachItem)
    #     print 'left course hour {}'.format((result_all_teacher[eachItem][key_value_1]-result_all_teacher[eachItem][key_value_2]))
    #     print 'left degree {}'.format((result_all_teacher[eachItem][key_value_3]-result_all_teacher[eachItem][key_value_4]))
    return result_list


def find_high_degree_course_count(result_list, count, result_all_teachers):
    tmp_list = []
    for eachItem in result_list:
        # print 'teacher id {} degree list {}'.format(eachItem, result_all_teachers[eachItem]['degree_list'])
        tmp_count = 0
        for eachCourse in result_all_teachers[eachItem]['degree_list']:
            if eachCourse >= 8:
                tmp_count += 1
        if tmp_count <= count:
            tmp_list.append(eachItem)
    return tmp_list


def balance_for_high_degree(result_all_teachers, result_left_courses, teacher_info, file_obj):
    print >>file_obj, '<STEP 2 high degree course balance>'
    high_degree_course_10 = []
    high_degree_course_9 = []
    high_degree_course_8 = []
    result_left_courses = sorted(result_left_courses, key=lambda x: x.course_degree, reverse=True)
    tmp_teacher_in_high_degree_course = []
    for eachCourse in result_left_courses:
        if eachCourse.course_degree == 10.0:
            high_degree_course_10.append(eachCourse)
        elif eachCourse.course_degree == 9.0:
            high_degree_course_9.append(eachCourse)
        elif eachCourse.course_degree == 8.0:
            high_degree_course_8.append(eachCourse)
        else:
            continue
    high_degree_course_10 = sort_new_1(high_degree_course_10)
    high_degree_course_9 = sort_new_1(high_degree_course_9)
    high_degree_course_8 = sort_new_1(high_degree_course_8)
    high_degree_course = [high_degree_course_10, high_degree_course_9, high_degree_course_8]
    for eachDegree in high_degree_course:
        for eachCourse in eachDegree:
            result_left_courses.remove(eachCourse)
            print >>file_obj, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print eachCourse.course_id
            teacher_list = eachCourse.suit_teacher.split(',')
            all_teachers = int(eachCourse.allow_teachers)
            teacher_without_high_degree = []
            teacher_with_high_degree = []
            teacher_id_list = []
            if eachCourse.semester == '一':
                tmp_str1 = 'total_hours_1'
                tmp_str2 = 'expect_hours_1'
                tmp_str3 = 'total_degree_1'
                tmp_str4 = 'expect_degree_1'
            else:
                tmp_str1 = 'total_hours_2'
                tmp_str2 = 'expect_hours_2'
                tmp_str3 = 'total_degree_2'
                tmp_str4 = 'expect_degree_2'
            for eachTeacher in teacher_list:
                teacher_id_list.append(teacher_info[eachTeacher]['id'])

            high_degree_count = 0
            for eachTeacher in teacher_id_list:
                print >>file_obj, 'teacher id {}'.format(eachTeacher)
                print >>file_obj, 'course list {}'.format(result_all_teachers[eachTeacher]['course_list'])
                print >>file_obj, 'degree list {}'.format(result_all_teachers[eachTeacher]['degree_list'])
                print >>file_obj, 'hour left {}'.format(
                    (result_all_teachers[eachTeacher][tmp_str2] - result_all_teachers[eachTeacher][tmp_str1]))
                print >>file_obj, 'degree left {}'.format(
                    (result_all_teachers[eachTeacher][tmp_str4] - result_all_teachers[eachTeacher][tmp_str3]))
            while all_teachers > 0:
                current_list = find_high_degree_course_count(teacher_id_list, high_degree_count, result_all_teachers)
                if len(current_list) > 1:
                    current_list = sort_new_2(current_list, result_all_teachers, tmp_str2, tmp_str1, tmp_str4, tmp_str3)
                if len(current_list) == 0:
                    high_degree_count += 1
                    continue
                print >>file_obj, 'current teacher list {}. high degree count {}'.format(current_list, high_degree_count)
                if result_all_teachers[current_list[0]][tmp_str1] + eachCourse.course_hour <= result_all_teachers[current_list[0]][tmp_str2]:
                    print >>file_obj, 'teacher id {}'.format(current_list[0])
                    print >>file_obj, 'total hours {}'.format(result_all_teachers[current_list[0]][tmp_str1])
                    print >>file_obj, 'degree list {}'.format(result_all_teachers[current_list[0]]['degree_list'])
                    result_all_teachers[current_list[0]]['course_list'].append(eachCourse.course_id)
                    result_all_teachers[current_list[0]]['degree_list'].append(eachCourse.course_degree)
                    result_all_teachers[current_list[0]][tmp_str1] += eachCourse.course_hour
                    result_all_teachers[current_list[0]][tmp_str3] += eachCourse.course_degree
                    all_teachers -= 1
                    print >>file_obj, 'new total hours {}'.format(result_all_teachers[current_list[0]][tmp_str1])
                    print >>file_obj, 'new degree list {}'.format(result_all_teachers[current_list[0]]['degree_list'])
                else:
                    high_degree_count += 1
                    if len(current_list) == len(teacher_id_list):
                        for i in range(all_teachers):
                            print >>file_obj, '<BAD SITUATION>'
                            print >>file_obj, 'teacher id {}'.format(current_list[i])
                            print >>file_obj, 'total hours {}'.format(result_all_teachers[current_list[i]][tmp_str1])
                            print >>file_obj, 'degree list {}'.format(result_all_teachers[current_list[i]]['degree_list'])
                            result_all_teachers[current_list[i]]['course_list'].append(eachCourse.course_id)
                            result_all_teachers[current_list[i]]['degree_list'].append(eachCourse.course_degree)
                            result_all_teachers[current_list[i]][tmp_str1] += eachCourse.course_hour
                            result_all_teachers[current_list[i]][tmp_str3] += eachCourse.course_degree
                            all_teachers -= 1
                            print >>file_obj, 'new total hours {}'.format(result_all_teachers[current_list[i]][tmp_str1])
                            print >>file_obj, 'new degree list {}'.format(result_all_teachers[current_list[i]]['degree_list'])

            print >>file_obj, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
    for eachItem in tmp_teacher_in_high_degree_course:
        print >>file_obj, '{} {}'.format(eachItem, result_all_teachers[eachItem]['degree_list'])
    # tmp = {}
    # for eachDegree in high_degree_course:
    #     for eachCourse in eachDegree:
    #         teacher_list = eachCourse.suit_teacher.split(',')
    #         for eachTeacher in teacher_list:
    #             if teacher_info[eachTeacher]['id'] not in tmp.keys():
    #                 tmp[teacher_info[eachTeacher]['id']] = [eachCourse.course_degree]
    #             else:
    #                 tmp[teacher_info[eachTeacher]['id']].append(eachCourse.course_degree)
    # for tmpKey in tmp.keys():
    #     print '{} {}'.format(tmpKey, tmp[tmpKey])
    return result_all_teachers, result_left_courses


def balance_for_course_hour(result_all_teachers, result_left_courses, teacher_info, file_obj):
    print >>file_obj, '<STEP 3 course hour balance>'
    for eachCourse in result_left_courses:
        print >>file_obj, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print eachCourse.course_id
        all_teachers = int(eachCourse.allow_teachers)
        if eachCourse.semester == '一':
            tmp_str1 = 'total_hours_1'
            tmp_str2 = 'expect_hours_1'
            tmp_str3 = 'total_degree_1'
            tmp_str4 = 'expect_degree_1'
        else:
            tmp_str1 = 'total_hours_2'
            tmp_str2 = 'expect_hours_2'
            tmp_str3 = 'total_degree_2'
            tmp_str4 = 'expect_degree_2'
        tmp = eachCourse.suit_teacher.split(',')
        teacher_list = []
        for eachTeacher in tmp:
            teacher_list.append(teacher_info[eachTeacher]['id'])
        for eachTeacher in teacher_list:
            print >>file_obj, 'teacher id {}'.format(eachTeacher)
            print >>file_obj, 'course list {}'.format(result_all_teachers[eachTeacher]['course_list'])
            print >>file_obj, 'degree list {}'.format(result_all_teachers[eachTeacher]['degree_list'])
            print >>file_obj, 'hour left {}'.format(
                (result_all_teachers[eachTeacher][tmp_str2] - result_all_teachers[eachTeacher][tmp_str1]))
            print >>file_obj, 'degree left {}'.format(
                (result_all_teachers[eachTeacher][tmp_str4] - result_all_teachers[eachTeacher][tmp_str3]))
        teacher_list = sort_new_2(teacher_list, result_all_teachers, tmp_str2, tmp_str1, tmp_str4, tmp_str3)
        for i in range(all_teachers):
            print >>file_obj, 'teacher id {}'.format(teacher_list[i])
            print >>file_obj, 'total hours {}'.format(result_all_teachers[teacher_list[i]][tmp_str1])
            print >>file_obj, 'degree list {}'.format(result_all_teachers[teacher_list[i]]['degree_list'])
            result_all_teachers[teacher_list[i]]['course_list'].append(eachCourse.course_id)
            result_all_teachers[teacher_list[i]]['degree_list'].append(eachCourse.course_degree)
            result_all_teachers[teacher_list[i]][tmp_str1] += eachCourse.course_hour
            result_all_teachers[teacher_list[i]][tmp_str3] += eachCourse.course_degree
            all_teachers -= 1
            print >>file_obj, 'new total hours {}'.format(result_all_teachers[teacher_list[i]][tmp_str1])
            print >>file_obj, 'new degree list {}'.format(result_all_teachers[teacher_list[i]]['degree_list'])

    return result_all_teachers, result_left_courses


@csrf_exempt
def arrange_export_report(request):
    now = datetime.now().strftime("%Y-%m-%d %H-%M")
    ws = xlwt.Workbook(encoding='utf-8')
    w = ws.add_sheet(u"排课结果")
    course_table = CourseInfo.objects.all()
    search_result = []
    for eachItem in course_table:
        search_result.append([eachItem.course_id, eachItem.course_name, eachItem.student_type,
                              eachItem.year, eachItem.class_name, eachItem.semester,
                              eachItem.course_hour, eachItem.course_degree, eachItem.student_type,
                              eachItem.allow_teachers, eachItem.times_every_week, eachItem.teacher_final_pick])

    table_head = ['代码', '名称', '学位', '年级', '班级', '学期', '学时', '难度', '必/选', '教师数', '周上课次数', '上课老师']
    for col, eachTitle in enumerate(table_head):
        w.write(0, col, eachTitle)
    for row, eachRow in enumerate(search_result):
        for col, eachCol in enumerate(eachRow):
            w.write(row+1, col, eachCol)
    exist_file = os.path.exists("last_report.xls")
    if exist_file:
        os.remove(r"last_report.xls")
    ws.save("last_report.xls")
    sio = BytesIO()
    ws.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename={}_{}.xls'.format('arrange_result', now)
    response.write(sio.getvalue())
    return response


@csrf_exempt
def arrange_export_analysis_1(request):
    now = datetime.now().strftime("%Y-%m-%d %H-%M")
    file_obj = open('analysis_result.txt', 'rb+').read()
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={}_{}.txt'.format('analysis_report_1', now)
    response.write(file_obj)
    return response


@csrf_exempt
def arrange_export_analysis_2(request):
    now = datetime.now().strftime("%Y-%m-%d %H-%M")
    total_info = start_arrange()
    file_obj = open('statistical_result.txt', 'wb+')
    file_obj.write('教师总数为: {}'.format(total_info[0][0]))
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={}_{}.txt'.format('analysis_report_1', now)
    response.write(file_obj)
    return response


@csrf_exempt
def arrange_search_by_course_id(request):
    course_id = request.POST['course_id']
    search_result = CourseInfo.objects.filter(course_id=course_id)
    if search_result:
        status = 'Success'
        course_name = search_result[0].course_name
        student_type = search_result[0].student_type
        semester = search_result[0].semester
        class_name = search_result[0].class_name
        course_degree = search_result[0].course_degree
        course_hour = search_result[0].course_hour
        times_every_week = search_result[0].times_every_week
        allow_teachers = search_result[0].allow_teachers
        teacher_pick = search_result[0].teacher_final_pick
        teacher_list = teacher_pick.split(',')
        tmp = []
        for eachTeacher in teacher_list:
            teacher_table = TeacherInfo.objects.filter(teacher_name=eachTeacher)
            if teacher_table:
                teacher_id = teacher_table[0].teacher_id
                tmp.append([teacher_id, eachTeacher])
            else:
                status = '原授课教师信息有误 {}'.format(eachTeacher)
        result = [course_name, student_type, semester, class_name, course_degree, course_hour, times_every_week,
                  allow_teachers, tmp]
    else:
        status = '找不到该课程号码对应的课程'

    result = json.dumps({'course': result, 'status': status})
    return HttpResponse(result)


@csrf_exempt
def arrange_change_by_course_id(request):
    course_id = request.POST['course_id']
    to_change_teacher = request.POST['to_change_teacher']
    try:
        CourseInfo.objects.filter(course_id=course_id).update(teacher_final_pick=to_change_teacher)
        status = 'Success'
    except Exception, e:
        print e
        status = '修改失败 错误信息{}'.format(e)
    result = json.dumps({'status': status})
    return HttpResponse(result)


@csrf_exempt
def arrange_change_button_status(request):
    button_id = request.POST['button_id']
    status = '确认微调过程失败'
    search_result = CurrentStepInfo.objects.all()
    if len(search_result) == 1:
        if button_id == 'adj_1':
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s4_teacher_confirm_u=1)
            status = 'Success'
        elif button_id == 'adj_2':
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s4_teacher_confirm_p1=1)
            status = 'Success'
        elif button_id == 'adj_3':
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s4_teacher_confirm_p2=1)
            status = 'Success'
        elif button_id == 'adj_4':
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s4_teacher_confirm_d=1)
            status = 'Success'
        else:
            pass

    result = json.dumps({'status': status})
    return HttpResponse(result)


@csrf_exempt
def arrange_step_5(request):
    operation_status = request.POST['status']
    search_result = CurrentStepInfo.objects.all()
    status = '切换至最后一步失败'
    if operation_status:
        if len(search_result) == 1:
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s5_status_flag=operation_status)
            status = 'Success'
    result = json.dumps({'status': status})
    return HttpResponse(result)



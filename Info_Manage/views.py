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
from datetime import datetime


@login_required()
def teacher_manage(request):
    teacher_table = TeacherInfo.objects.all()
    search_result = []
    for eachItem in teacher_table:
        search_result.append([eachItem.teacher_id, eachItem.teacher_name, eachItem.first_semester_expect, eachItem.second_semester_expect,
                             eachItem.first_semester, eachItem.second_semester])
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
    teacher_list = []
    line_width = work_sheet.row_len(0)
    for line_number in range(line_length):
        teacher_id, teacher_name = work_sheet.row(line_number)
        if type(teacher_id.value) == float:
            teacher_list.append([int(teacher_id.value), teacher_name.value])
    insert_teacher_list_into_db(teacher_list)
    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


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
    now = datetime.now()
    search_result = CourseInfo.objects.all().filter(course_id=course_info[0])
    if search_result:
        CourseInfo.objects.filter(course_id=course_info[0]).update(course_id=course_info[0],course_name=course_info[1], student_type=course_info[2],
                                                                    year=course_info[3], class_name=course_info[4], semester=course_info[5],
                                                                    course_hour=course_info[6], course_degree=course_info[7], course_type=course_info[8],
                                                                    allow_teachers=course_info[9], times_every_week=course_info[10], suit_teacher=course_info[11], teacher_ordered=course_info[12], update_time=now)
    else:
        CourseInfo.objects.create(course_id=course_info[0], course_name=course_info[1], student_type=course_info[2],
                                   year=course_info[3], class_name=course_info[4], semester=course_info[5],
                                   course_hour=course_info[6], course_degree=course_info[7], course_type=course_info[8],
                                   allow_teachers=course_info[9], times_every_week=course_info[10], suit_teacher=course_info[11], teacher_ordered=course_info[12],update_time=now)


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
        course_name  = eachLine[8].value
        student_type = eachLine[3].value
        year = eachLine[1].value
        class_name = eachLine[5].value
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
    for eachCourse in class_info_to_save:
        save_course_into_database(eachCourse)


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
    [degree_count_u, degree_count_p1, degree_count_p2, degree_count_d] = [[0]*10,[0]*10,[0]*10,[0]*10]
    [hours_u, hours_p1, hours_p2, hours_d] = [[], [], [], []]
    total_hours = 0
    total_courses = len(search_result_course)
    for eachCourse in search_result_course:
        degree_count[int(eachCourse.course_degree)-1] += 1
        total_hours += eachCourse.course_hour
        if eachCourse.student_type == '博士':
            degree_count_d[int(eachCourse.course_degree)-1] += 1
            hours_d.append(eachCourse.course_hour)
        elif eachCourse.student_type == '法律硕士':
            degree_count_p2[int(eachCourse.course_degree)-1] += 1
            hours_p2.append(eachCourse.course_hour)
        elif eachCourse.student_type == '法学硕士':
            degree_count_p1[int(eachCourse.course_degree) - 1] += 1
            hours_p1.append(eachCourse.course_hour)
        elif eachCourse.student_type == '本科':
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
    tmp_u,tmp_p1,tmp_p2,tmp_d = [0]*4,[0]*4,[0]*4,[0]*4
    for index,item in enumerate([18,36,54,72]):
        tmp_d[index] = hours_d.count(item)
        tmp_p1[index] = hours_p1.count(item)
        tmp_p2[index] = hours_p2.count(item)
        tmp_u[index] = hours_u.count(item)
    degree_count_u.extend(tmp_u)
    degree_count_p1.extend(tmp_p1)
    degree_count_p2.extend(tmp_p2)
    degree_count_d.extend(tmp_d)
    return [teacher_count,teacher_with_expect_count, total_hours_with_expect, teacher_without_expect_count, round(ave_hours_without_expect, 2),
            degree_count, total_courses, [degree_count_u, degree_count_p1, degree_count_p2, degree_count_d]]


def arrange_main():
    search_result_course = CourseInfo.objects.all()
    search_result_teacher = TeacherInfo.objects.all()
    teacher_1 = {}
    teacher_2 = {}
    result_1 = {}
    result_2 = []
    for eachTeacher in search_result_teacher:
        teacher_1[eachTeacher.teacher_name] = eachTeacher.teacher_id
        teacher_2[eachTeacher.teacher_id] = eachTeacher.teacher_name
    for eachCourse in search_result_course:
        tmp_dict = {'course_list': [], 'degree_list': [], 'total_hours': 0, 'expect_hours': 191}  #todo
        teacher_list = eachCourse.suit_teacher.split(',')
        if len(teacher_list) == int(eachCourse.allow_teachers):
            for eachTeacher in teacher_list:
                if teacher_1[eachTeacher] in result_1.keys():
                    result_1[teacher_1[eachTeacher]]['course_list'].append(eachCourse.course_id)
                    result_1[teacher_1[eachTeacher]]['degree_list'].append(eachCourse.course_degree)
                    result_1[teacher_1[eachTeacher]]['total_hours'] += int(eachCourse.course_hour)
                else:
                    tmp_dict['course_list'] = [eachCourse.course_id]
                    tmp_dict['degree_list'] = [eachCourse.course_degree]
                    tmp_dict['total_hours'] = int(eachCourse.course_hour)
                    result_1[teacher_1[eachTeacher]] = tmp_dict
        else:
            result_2.append(eachCourse)
    show_statistical(result_1, result_2)
    result_2 = sorted(result_2, key=lambda x: x.course_degree, reverse=True)
    for eachCourse in result_2:
        tmp_dict = {'course_list': [], 'degree_list': [], 'total_hours': 0, 'expect_hours': 191}  # todo
        teacher_list = eachCourse.suit_teacher.split(',')
        allow_teacher = int(eachCourse.allow_teachers)
        for eachTeacher in teacher_list:
            if teacher_1[eachTeacher] not in result_1.keys():
                tmp_dict['course_list'] = [eachCourse.course_id]
                tmp_dict['degree_list'] = [eachCourse.course_degree]
                tmp_dict['total_hours'] = int(eachCourse.course_hour)
                result_1[teacher_1[eachTeacher]] = tmp_dict
            else:
                if result_1[teacher_1[eachTeacher]]['total_hours'] + eachCourse.course_hour < result_1[teacher_1[eachTeacher]]['expect_hours']:
                    if eachCourse.course_degree not in result_1[teacher_1[eachTeacher]]['degree_list'] or eachCourse.course_degree < 8:
                        result_1[teacher_1[eachTeacher]]['course_list'].append(eachCourse.course_id)
                        result_1[teacher_1[eachTeacher]]['degree_list'].append(eachCourse.course_degree)
                        result_1[teacher_1[eachTeacher]]['total_hours'] += int(eachCourse.course_hour)
            allow_teacher -= 1
            if allow_teacher == 0:
                result_2.remove(eachCourse)
                break
    show_statistical(result_1, result_2)
    for tmpKey in result_1.keys():
        while result_1[tmpKey]['total_hours'] < result_1[tmpKey]['expect_hours']:
            for eachCourse in result_2:
                teacher_list = eachCourse.suit_teacher.split(',')
                allow_teacher = int(eachCourse.allow_teachers)
                if allow_teacher == 1:
                    if teacher_2[tmpKey] not in teacher_list:
                        continue
                    else:
                        if result_1[tmpKey]['total_hours']+int(eachCourse.course_hour) < result_1[tmpKey]['expect_hours']:
                            result_1[tmpKey]['course_list'].append(eachCourse.course_id)
                            result_1[tmpKey]['degree_list'].append(eachCourse.course_degree)
                            result_1[tmpKey]['total_hours'] += int(eachCourse.course_hour)
                            result_2.remove(eachCourse)
                else:
                    continue
            break
    show_statistical(result_1, result_2)
    result_3 = {}
    for tmpKey in result_1.keys():
        for eachCourse in result_1[tmpKey]['course_list']:
            if CourseInfo.objects.get(course_id=eachCourse).semester == '一':
                TeacherInfo.objects.filter(teacher_id=tmpKey).update(first_semester=result_1[tmpKey]['total_hours'])
            else:
                TeacherInfo.objects.filter(teacher_id=tmpKey).update(second_semester=result_1[tmpKey]['total_hours'])
            if eachCourse not in result_3.keys():
                result_3[eachCourse] = [teacher_2[tmpKey]]
            else:
                result_3[eachCourse].append(teacher_2[tmpKey])
    for tmpKey in result_3.keys():
        tmp = ",".join(result_3[tmpKey])
        CourseInfo.objects.filter(course_id=tmpKey).update(teacher_auto_pick=tmp)

    return result_1


def show_statistical(result_1, result_2):
    hours_larger = 0
    for tmpKey in result_1.keys():
        if result_1[tmpKey]['total_hours'] > result_1[tmpKey]['expect_hours']:
            hours_larger += 1
    print '######################'
    print '## {}'.format(hours_larger)
    print '######################'

    course_left = len(result_2)
    print '######################'
    print '## {}'.format(course_left)
    print '######################'

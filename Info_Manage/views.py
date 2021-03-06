# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.http import urlquote
from django.db import connection

from Info_Manage.models import TeacherInfo, CourseInfo, CurrentStepInfo, CourseHistoryInfo, CourseAdjustInfo
# Create your views here.

import os
import sys
import xlrd
import math
import random
from datetime import datetime
import xlwt
import logging
from logging.handlers import TimedRotatingFileHandler

from io import StringIO, BytesIO
from myLogger import MyLogger

reload(sys)
sys.setdefaultencoding('utf-8')

STUDENT_TYPE = ['本科', '法学硕士', 'JM', '法学博士']
CLASS_NAME_LIST = ["第二专业教学", "通识教育","法学专业教育", "跨校辅修教学", "基础教育", "法律硕士(法学)", "法律硕士(非法学)1班",
                   "法律硕士(非法学)2班", "法律硕士在职生", "法律史", "法学理论", "国际法学", "环境与资源保护法学", "经济法学",
                   "民商法学", "诉讼法学", "刑法学", "宪法学与行政法学", "法律硕士（法学）国际班", "法律硕士（非法学）国际班"]
CLASS_GRADE = [str(datetime.now().year - i) for i in [2000, 2001, 2002, 2003]]
SEMESTER = ['一', '二']
COURSE_HOUR = ['18', '36', '54', '56', '72']
COURSE_DEGREE = ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10']
COURSE_TYPE = ['必修', '选修']
LANGUAGE = ['中文', '英文', '中/英']
current_school_year = '{}-{}'.format(datetime.now().year, datetime.now().year+1)
DEBUG = True
#######################################################
log_file_handler = TimedRotatingFileHandler(filename="test.log", when="M", interval=1, backupCount=10)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='test.log', level=logging.DEBUG, format=LOG_FORMAT)
log = logging.getLogger()
log.addHandler(log_file_handler)
#######################################################
module_log_update = MyLogger()


@login_required()
def teacher_manage(request):
    if request.user.nickname == 'leader':
        user_type = 'leader'
    else:
        user_type = 'teacher'
    search_result = CurrentStepInfo.objects.all()

    if search_result:
        year = search_result[0].s1_year_info
    else:
        year = 'None'
    teacher_table = TeacherInfo.objects.filter()
    course_table = CourseInfo.objects.filter(lock_state=0)
    search_result = []
    weight_total_1 = 1
    weight_total_2 = 1
    apply_done = 0
    apply_done_not_satisfy = 0
    lock_teacher_count = 0
    for eachItem in teacher_table:
        apply_course_count = 0
        for eachCourse in course_table:
            if eachCourse.course_relate and eachCourse.student_type != '本科':
                continue
            teacher_order_list = eachCourse.teacher_ordered.split(',')
            if eachItem.teacher_name in teacher_order_list:
                apply_course_count += 1
        search_result.append([eachItem.teacher_id,
                              eachItem.teacher_name,
                              eachItem.major,
                              eachItem.teacher_type,
                              eachItem.teacher_title,
                              eachItem.birthday,
                              eachItem.first_semester_expect*100,
                              eachItem.second_semester_expect*100,
                              eachItem.first_semester_hours if eachItem.first_semester_hours else 0,
                              eachItem.second_semester_hours if eachItem.second_semester_hours else 0,
                              eachItem.first_semester_degree if eachItem.first_semester_degree else 0,
                              eachItem.second_semester_degree if eachItem.second_semester_degree else 0,
                              eachItem.teacher_apply_done,
                              eachItem.notes if eachItem.notes else '',
                              apply_course_count,
                              eachItem.lock_state
                              ])
        if eachItem.lock_state == 1:
            lock_teacher_count += 1
        else:
            if eachItem.teacher_apply_done and ( eachItem.teacher_apply_done == '申报结束' or eachItem.teacher_apply_done == '申报结束/不满足申报要求'):
                apply_done += 1
                if eachItem.teacher_apply_done == '申报结束/不满足申报要求':
                    apply_done_not_satisfy += 1
            weight_total_1 += eachItem.first_semester_expect
            weight_total_2 += eachItem.second_semester_expect
    current_teacher_count = len(search_result)
    total_hours_1 = 0
    total_hours_2 = 0
    total_degree_1 = 0
    total_degree_2 = 0
    for eachItem in course_table:
        tmp_hour,tmp_degree = get_course_effective_point(eachItem)
        if eachItem.semester == '一':
            total_hours_1 += tmp_hour
            total_degree_1 += tmp_degree
        else:
            total_hours_2 += tmp_hour
            total_degree_2 += tmp_degree
    expect_hours_for_semester1 = math.ceil((total_hours_1/weight_total_1)/18)*18
    expect_hours_for_semester2 = math.ceil((total_hours_2/weight_total_2)/18)*18
    expect_degree_for_semester1 = round(total_degree_1/weight_total_1, 2)
    expect_degree_for_semester2 = round(total_degree_2/weight_total_2, 2)

    summary_table = [current_teacher_count, apply_done, expect_hours_for_semester1, expect_hours_for_semester2,
                     expect_degree_for_semester1, expect_degree_for_semester2, lock_teacher_count, apply_done_not_satisfy]
    table_head = ['教师代码', '教师姓名', '学科组','职称','导师类型','出生年月','期望学时1(%)', '期望学时2(%)', '已分配学时1', '已分配学时2','已分配难度1',
                  '已分配难度2' ,'申报完成', '特殊理由', '已申报课程数','状态']
    return render(request, 'teacher_manage_apply.html', {'UserName': request.user.last_name+request.user.first_name+request.user.username,
                                                   'teacher_table': search_result, 'summary_table': summary_table,
                                                   'table_head': table_head, 'year': year, 'user_type':user_type})

@login_required
def teacher_manage_adjust(request):
    if request.user.nickname == 'leader':
        user_type = 'leader'
    else:
        user_type = 'teacher'
    search_result = CurrentStepInfo.objects.all()
    if search_result:
        year = search_result[0].s1_year_info
    else:
        year = 'None'
    course_adjust_table = CourseAdjustInfo.objects.all()
    search_result = []
    for eachLine in course_adjust_table:
        course_id = eachLine.course_id
        course_name = eachLine.course_name
        teacher_before = eachLine.teacher_before
        teacher_after = eachLine.teacher_after
        status = eachLine.status
        notes = eachLine.notes
        search_result.append([course_id, course_name, teacher_before, teacher_after, status, notes])
    table_head = ['课程代码', '课程名称', '原授课教师', '微调教师', '申请状态', '补充说明']
    return render(request, 'teacher_manage_adjust.html',
                  {'UserName': request.user.last_name + request.user.first_name + request.user.username,
                   'teacher_table': search_result,
                   'table_head': table_head,
                   'year': year,
                   'user_type': user_type})

@login_required
def teacher_leader(request):
    if request.user.nickname == 'leader':
        user_type = 'leader'
    else:
        user_type = 'teacher'
    search_result = CurrentStepInfo.objects.all()
    if search_result:
        year = search_result[0].s1_year_info
    else:
        year = 'None'
    course_adjust_table = CourseAdjustInfo.objects.all()
    search_result = []
    for eachLine in course_adjust_table:
        course_id = eachLine.course_id
        course_name = eachLine.course_name
        teacher_before = eachLine.teacher_before
        teacher_after = eachLine.teacher_after
        status = eachLine.status
        notes = eachLine.notes
        if status != '等待审批':
            continue
        search_result.append([course_id, course_name, teacher_before, teacher_after, status, notes])
    table_head = ['课程代码', '课程名称', '原授课教师', '微调教师', '申请状态', '补充说明']
    return render(request, 'teacher_leader.html', {'UserName': request.user.last_name+request.user.first_name+request.user.username,
                                                   'teacher_table': search_result,
                                                   'table_head': table_head,
                                                   'year': year,
                                                   'user_type':user_type})

@csrf_exempt
def teacher_reject_teacher_adjust(request):
    course_id = request.POST['course_id']
    reject_notes = request.POST['notes']
    search_result = CourseAdjustInfo.objects.filter(course_id=course_id)
    user = request.user.last_name + request.user.first_name + request.user.username
    if search_result:
        CourseAdjustInfo.objects.filter(course_id=course_id).update(status='已驳回', notes=reject_notes)
        module_log_update.data_operate_log(user, '[CourseAdjustInfo] course_id {} status: {} notes: {}'.format(course_id, '已驳回', reject_notes))
        status = '驳回微调申请'
    else:
        status = '课程代码异常'
    result = json.dumps({'status': status})
    return HttpResponse(result)

@csrf_exempt
def teacher_approve_teacher_adjust(request):
    course_id = request.POST['course_id']
    user = request.user.last_name + request.user.first_name + request.user.username

    search_result = CourseAdjustInfo.objects.filter(course_id=course_id)
    if search_result:
        to_change_teacher = search_result[0].teacher_after

        notes = search_result[0].notes
        try:
            search_result = CourseInfo.objects.filter(course_id=course_id)
            final_teacher_list = search_result[0].teacher_final_pick.split(',') if search_result[0].teacher_final_pick else []
            # course_hour = search_result[0].course_hour / (len(final_teacher_list) if final_teacher_list else 1)
            # course_degree = search_result[0].course_degree / (len(final_teacher_list if final_teacher_list else 1))

            course_hour = (search_result[0].course_hour * int(search_result[0].course_parallel)) / (
                len(final_teacher_list) if final_teacher_list else 1)
            course_degree = (search_result[0].course_degree * int(search_result[0].course_parallel)) / (
                len(final_teacher_list) if final_teacher_list else 1)

            semester = search_result[0].semester
            for eachTeacher in final_teacher_list:
                teacher_result = TeacherInfo.objects.filter(teacher_name=eachTeacher)
                if semester == '一':
                    value1 = float(teacher_result[0].first_semester_hours if teacher_result[0].first_semester_hours else 0) - float(course_hour)
                    value2 = float(teacher_result[0].first_semester_degree if teacher_result[0].first_semester_degree else 0) - float(course_degree)
                    TeacherInfo.objects.filter(teacher_name=eachTeacher).update(first_semester_hours=value1,
                                                                                first_semester_degree=value2)
                    module_log_update.data_operate_log(user, '[TeacherInfo] teacher_name: {} first_semester_hours: {} first_semester_degree: {}'.format(
                        eachTeacher,
                        value1,
                        value2
                    ))
                else:
                    value1 = float(teacher_result[0].second_semester_hours if teacher_result[0].second_semester_hours else 0) - float(course_hour)
                    value2 = float(teacher_result[0].second_semester_degree if teacher_result[0].second_semester_degree else 0) - float(course_degree)
                    TeacherInfo.objects.filter(teacher_name=eachTeacher).update(second_semester_hours=value1,
                                                                                second_semester_degree=value2)
                    module_log_update.data_operate_log(user, '[TeacherInfo] teacher_name: {} second_semester_hours: {} second_semester_degree: {}'.format(
                        eachTeacher,
                        value1,
                        value2
                    ))
            to_change_teacher_list = to_change_teacher.split(',')
            tmp_change_teacher_list = []
            for eachTeacher in to_change_teacher_list:
                eachTeacher = eachTeacher.split('(')[0]
                tmp_change_teacher_list.append(eachTeacher)
                teacher_result = TeacherInfo.objects.filter(teacher_name=eachTeacher)
                if semester == '一':

                    value1 = float(teacher_result[0].first_semester_hours if teacher_result[0].first_semester_hours else 0) + float(course_hour)
                    value2 = float(teacher_result[0].first_semester_degree if teacher_result[0].first_semester_degree else 0) + float(course_degree)
                    TeacherInfo.objects.filter(teacher_name=eachTeacher).update(first_semester_hours=value1,
                                                                                first_semester_degree=value2)
                    module_log_update.data_operate_log(user, '[TeacherInfo] teacher_name: {} first_semester_hours: {} first_semester_degree: {}'.format(
                        eachTeacher,
                        value1,
                        value2
                    ))
                else:
                    value1 = float(teacher_result[0].second_semester_hours if teacher_result[0].second_semester_hours else 0) + float(course_hour)
                    value2 = float(teacher_result[0].second_semester_degree if teacher_result[0].second_semester_degree else 0) + float(course_degree)
                    TeacherInfo.objects.filter(teacher_name=eachTeacher).update(second_semester_hours=value1,
                                                                                second_semester_degree=value2)
                    module_log_update.data_operate_log(user, '[TeacherInfo] teacher_name: {} second_semester_hours: {} second_semester_degree: {}'.format(
                        eachTeacher,
                        value1,
                        value2
                    ))

            tmp_change_teacher = ','.join(tmp_change_teacher_list)
            CourseInfo.objects.filter(course_id=course_id).update(teacher_final_pick=tmp_change_teacher)
            module_log_update.data_operate_log(user, '[CourseInfo]course_id:{} teacher_final_pick: {}'.format(course_id, tmp_change_teacher))

            search_result_course = CourseInfo.objects.filter(course_id=course_id)
            if search_result_course[0].course_relate:
                course_list = search_result_course[0].course_relate.split(',')
                for eachCourse in course_list:
                    CourseInfo.objects.filter(course_id=eachCourse).update(teacher_final_pick=tmp_change_teacher)
                    module_log_update.data_operate_log(user,
                                               '[CourseInfo]current course: {} course_relate:{} teacher_final_pick: {}'.format(course_id,
                                                                                                                        eachCourse,
                                                                                                                        tmp_change_teacher))
            status = '已批准'
            CourseAdjustInfo.objects.filter(course_id=course_id).update(status='已批准')
            module_log_update.data_operate_log(user, '[CourseAdjustInfo] course_id {} status: 已批准'.format(course_id))
        except Exception, e:
            print e
            status = '修改失败 错误信息{}'.format(e)
    else:
        status = '课程代码异常: {}'.format(course_id)
    result = json.dumps({'status': status})
    return HttpResponse(result)


@csrf_exempt
def teacher_save_and_config(request):
    user = request.user.last_name + request.user.first_name + request.user.username
    teacher_table = json.loads(request.POST['teacher_table'])
    data_length = teacher_table['length']
    all_teacher = []
    for i in range(data_length):
        all_teacher.append(teacher_table[str(i)])

    save_teacher_into_database(all_teacher, user)
    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def save_teacher_into_database(all_teacher, user=''):
    now = datetime.now()
    for eachItem in all_teacher:
        search_result = TeacherInfo.objects.all().filter(teacher_id=eachItem[0])
        if search_result:
            TeacherInfo.objects.filter(teacher_id=eachItem[0]).update(teacher_name=eachItem[1], first_semester=eachItem[2],
                                                                      second_semester=eachItem[3], claiming_course=eachItem[4], update_time=now)
            module_log_update.data_operate_log(user, '[TeacherInfo] update teacher_id: {} teacher_name: {} first_semester: {} second_semester: {} claiming_course: {}'.format(
                eachItem[0],
                eachItem[1],
                eachItem[2],
                eachItem[3],
                eachItem[4]
            ))
        else:
            TeacherInfo.objects.create(teacher_id=eachItem[0], teacher_name=eachItem[1], first_semester=eachItem[2],
                                       second_semester=eachItem[3], claiming_course=eachItem[4], update_time=now)
            module_log_update.data_operate_log(user, '[TeacherInfo] create teacher_id: {} teacher_name: {} first_semester: {} second_semester: {} claiming_course: {}'.format(
                eachItem[0],
                eachItem[1],
                eachItem[2],
                eachItem[3],
                eachItem[4]
            ))


@login_required()
def teacher_personal_lock(request):
    search_result = TeacherInfo.objects.filter(teacher_id=request.user.username)
    status = 'free'
    user_type = 'teacher'
    current_arrange_status = ''
    if search_result:
        if search_result[0].teacher_apply_done:
            status = 'recall'
            if search_result[0].teacher_apply_done == '申报结束/申请撤回申报完成':
                status = 'wait_approve'
    if request.user.nickname == 'leader':
        user_type = 'leader'

    now = datetime.now().replace()
    search_result_major = CourseInfo.objects.values('major')
    search_result_teacher_major = TeacherInfo.objects.filter(teacher_id=request.user.username)
    major_list = []
    for row_major in search_result_major:
        if row_major['major']:
            major_list.append(row_major['major'])
    major_set = set(major_list)
    major_list = []
    current_teacher_major = []
    if search_result_teacher_major:
        current_teacher_major = search_result_teacher_major[0].major.split(',')
    for each_set in major_set:
        if each_set in current_teacher_major:
            if each_set == '综合':
                major_list.insert(0,['1', each_set])
            else:
                major_list.append(["1", each_set])
        else:
            if each_set == '综合':
                major_list.insert(0,['0', each_set])
            else:
                major_list.append(["0", each_set])
    search_result = CurrentStepInfo.objects.all()
    if search_result and search_result[0].s2_deadline:
        delta = (search_result[0].s2_deadline.replace(tzinfo=None) - now).total_seconds()
        if delta < 0.0:
            status = 'lock'
    if search_result:
        year = search_result[0].s1_year_info
        current_arrange_status = search_result[0].s5_status_flag
    else:
        year = 'None'
    search_result = []
    if current_arrange_status != 'lock done':
        return render(request, 'teacher_personal_lock.html',
                      {'UserName': request.user.last_name + request.user.first_name + request.user.username,
                       'class_table': search_result,
                       'table_head': [],
                       'summary_table': [-1],
                       'year': year,
                       'status': status,
                       'major_list': major_list,
                       'user_type': user_type})
    else:
        current_user_selected = CourseInfo.objects.filter(teacher_final_pick__contains=request.user.last_name+request.user.first_name)
        for eachItem in current_user_selected:
            if eachItem.course_relate and eachItem.student_type != '本科':
                continue
            class_name_list = eachItem.class_name.split(' ')
            if eachItem.course_relate and eachItem.student_type == '本科':
                course_relate_list = eachItem.course_relate.split(',')
                for eachCourseId in course_relate_list:
                    if CourseInfo.objects.filter(course_id=eachCourseId):
                        class_name_list.extend(CourseInfo.objects.filter(course_id=eachCourseId)[0].class_name.split(' '))
            # todo when class name confirm, may change
            # class_name_str = ' / '.join((' '.join(class_name_list)).split(' '))
            class_name_str = get_class_name(class_name_list)
            if request.user.last_name + request.user.first_name in eachItem.teacher_ordered.split(',') \
                    and request.user.last_name + request.user.first_name != '':
                tmp = '已分配(已申报)'
            else:
                tmp = '已分配(未申报)'
            if eachItem.course_relate:
                course_relate = eachItem.course_relate.strip(',')
                course_id_str = '{} / {}'.format(eachItem.course_id, course_relate)
                student_type_relate = CourseInfo.objects.filter(course_id=course_relate)[0].student_type
                student_type_str = '{} / {}'.format(eachItem.student_type, student_type_relate)
            else:
                course_id_str = eachItem.course_id
                student_type_str = eachItem.student_type

            search_result.append([course_id_str,
                                  eachItem.course_name,
                                  eachItem.major,
                                  student_type_str,
                                  class_name_str,
                                  eachItem.semester,
                                  eachItem.course_hour,
                                  eachItem.course_degree,
                                  eachItem.course_type,
                                  eachItem.language,
                                  eachItem.allow_teachers,
                                  eachItem.times_every_week,
                                  eachItem.course_parallel,
                                  get_excellent_course(eachItem.excellent_course),
                                  tmp])
    search_result_teacher = TeacherInfo.objects.filter(teacher_id=request.user.username)
    if search_result_teacher:
        expect_semester1 = str(search_result_teacher[0].first_semester_expect*100)
        expect_semester2 = str(search_result_teacher[0].second_semester_expect*100)
    else:
        expect_semester1 = 0
        expect_semester2 = 0
    summary_table = [expect_semester1, expect_semester2]
    table_head = ['代码', '名称', '专业','学位', '班级', '学期', '学时', '难度', '必/选', '语言','教师数', '周上课次数','平行班级','是否精品课程','课程状态']
    # table_default = ['', '', major_set, STUDENT_TYPE, CLASS_NAME_LIST, ['一', '二'], COURSE_HOUR, COURSE_DEGREE, ['必修', '选修'], LANGUAGE, '', '', '']
    return render(request, 'teacher_personal_lock.html', {'UserName': request.user.last_name+request.user.first_name+request.user.username,
                                                     'class_table': search_result,
                                                     'table_head': table_head,
                                                     'summary_table': summary_table,
                                                     'year': year,
                                                     'status': status,
                                                     'major_list':major_list,
                                                     'user_type': user_type})


def get_class_name(class_name_list):
    tmp_class_list = []
    for eachClass in class_name_list:
        student_type = eachClass.split('-')[0]
        class_name = eachClass.split('-')[-1].split('_')[-1]
        grade = eachClass.split('-')[-1].split('_')[0]
        tmp_class_list.append('{}{}{}'.format(student_type, grade, class_name))
    return " / ".join(tmp_class_list)


def get_excellent_course(excellent_course):
    if excellent_course not in ['校级精品课程','上海市精品课程','国家级精品开放课程']:
        return ''
    else:
        return excellent_course


@login_required()
def teacher_personal(request):
    search_result = TeacherInfo.objects.filter(teacher_id=request.user.username)
    status = 'free'
    user_type = 'teacher'
    current_arrange_status = ''
    if search_result:
        if search_result[0].teacher_apply_done:
            status = 'recall'
            if search_result[0].teacher_apply_done == '申报结束/申请撤回申报完成':
                status = 'wait_approve'
    if request.user.nickname == 'leader':
        user_type = 'leader'

    now = datetime.now().replace()
    search_result_major = CourseInfo.objects.values('major')
    search_result_teacher_major = TeacherInfo.objects.filter(teacher_id=request.user.username)
    major_list = []
    for row_major in search_result_major:
        if row_major['major']:
            major_list.append(row_major['major'])
    major_set = set(major_list)
    major_list = []
    current_teacher_major = []
    if search_result_teacher_major:
        current_teacher_major = search_result_teacher_major[0].major.split(',')
    for each_set in major_set:
        if each_set in current_teacher_major:
            if each_set == '综合':
                major_list.insert(0,['1', each_set])
            else:
                major_list.append(["1", each_set])
        else:
            if each_set == '综合':
                major_list.insert(0,['0', each_set])
            else:
                major_list.append(["0", each_set])
    search_result = CurrentStepInfo.objects.all()
    if search_result and search_result[0].s2_deadline:
        delta = (search_result[0].s2_deadline.replace(tzinfo=None) - now).total_seconds()
        if delta < 0.0:
            status = 'lock'
    if search_result:
        year = search_result[0].s1_year_info
        current_arrange_status = search_result[0].s5_status_flag
    else:
        year = 'None'
    search_result = []
    for each_major in current_teacher_major:
        course_table = CourseInfo.objects.all().filter(major__contains=each_major, lock_state=0)
        tmp = ''
        for eachItem in course_table:
            if eachItem.course_relate and eachItem.student_type != '本科':
                continue
            class_name_list = eachItem.class_name.split(' ')
            if eachItem.course_relate and eachItem.student_type == '本科':
                course_relate_list = eachItem.course_relate.split(',')
                for eachCourseId in course_relate_list:
                    if CourseInfo.objects.filter(course_id=eachCourseId):
                        class_name_list.extend(CourseInfo.objects.filter(course_id=eachCourseId)[0].class_name.split(' '))
            # todo when class name confirm, may change
            class_name_str = get_class_name(class_name_list)
            # class_name_str = ' / '.join((' '.join(class_name_list)).split(' '))
            if request.user.last_name+request.user.first_name in eachItem.teacher_ordered.split(',') \
                    and request.user.last_name+request.user.first_name != '':
                tmp = '已申报'
            else:
                tmp = ''
            if eachItem.course_relate:
                course_relate = eachItem.course_relate.strip(',')
                course_id_str = '{} / {}'.format(eachItem.course_id, course_relate)
                student_type_relate = CourseInfo.objects.filter(course_id=course_relate)[0].student_type
                student_type_str = '{} / {}'.format(eachItem.student_type, student_type_relate)
            else:
                course_id_str = eachItem.course_id
                student_type_str = eachItem.student_type

            search_result.append([course_id_str,
                                  eachItem.course_name,
                                  eachItem.major,
                                  student_type_str,
                                  class_name_str,
                                  eachItem.semester,
                                  eachItem.course_hour,
                                  eachItem.course_degree,
                                  eachItem.course_type,
                                  eachItem.language,
                                  eachItem.allow_teachers,
                                  eachItem.times_every_week,
                                  eachItem.course_parallel,
                                  get_excellent_course(eachItem.excellent_course),
                                  tmp])
    search_result_teacher = TeacherInfo.objects.filter(teacher_id=request.user.username)
    if search_result_teacher:
        expect_semester1 = str(search_result_teacher[0].first_semester_expect*100)
        expect_semester2 = str(search_result_teacher[0].second_semester_expect*100)
    else:
        expect_semester1 = 0
        expect_semester2 = 0
    summary_table = [expect_semester1, expect_semester2]
    table_head = ['代码', '名称', '专业','学位', '班级', '学期', '学时', '难度', '必/选', '语言','教师数', '周上课次数','平行班级','是否精品课程','课程状态']
    # table_default = ['', '', major_set, STUDENT_TYPE, CLASS_NAME_LIST, ['一', '二'], COURSE_HOUR, COURSE_DEGREE, ['必修', '选修'], LANGUAGE, '', '', '']
    return render(request, 'teacher_personal.html', {'UserName': request.user.last_name+request.user.first_name+request.user.username,
                                                     'class_table': search_result,
                                                     'table_head': table_head,
                                                     'summary_table': summary_table,
                                                     'year': year,
                                                     'status': status,
                                                     'major_list':major_list,
                                                     'user_type': user_type})


@csrf_exempt
def teacher_request_course(request):
    user = request.user.last_name + request.user.first_name + request.user.username
    course_id = request.POST['course_id']
    searchResult = TeacherInfo.objects.filter(teacher_id=request.user.username)
    if searchResult:
        teacher_name = searchResult[0].teacher_name
    else:
        teacher_name = '教务员'
    now = datetime.now().replace()
    search_result = CurrentStepInfo.objects.all()
    if search_result and search_result[0].s2_deadline:
        delta = (search_result[0].s2_deadline.replace(tzinfo=None) - now).total_seconds()
        if delta < 0.0:
            status = '申报时间已经截至, 无法再申报或者取消课程'
            result = json.dumps({'status': status})
            return HttpResponse(result)
    if 'status' not in request.POST.keys():
        status = save_teacher_to_course_info(course_id, teacher_name, user)
    else:
        status = remove_teacher_from_course_info(course_id, teacher_name, user)
    # TODO: result part
    result = json.dumps({'status': status})
    return HttpResponse(result)


@csrf_exempt
def teacher_change_expect(request):
    user = request.user.last_name + request.user.first_name + request.user.username
    modify_0 = request.POST['modify_0'] if request.POST['modify_0'] else 0
    modify_1 = request.POST['modify_1'] if request.POST['modify_1'] else 0
    lock_state = request.POST['lock_state'] if 'lock_state' in request.POST else 0
    modify_0 = float(modify_0) / 100.0
    modify_1 = float(modify_1) / 100.0
    if 'teacher_id' in request.POST.keys():
        teacher_id = request.POST['teacher_id']
    else:
        teacher_id = request.user.username
    searchResult = TeacherInfo.objects.filter(teacher_id=teacher_id)
    status = '修改期望失败'
    if searchResult:
        TeacherInfo.objects.filter(teacher_id=teacher_id).update(first_semester_expect=modify_0,
                                                                 second_semester_expect=modify_1,
                                                                 lock_state=lock_state)
        module_log_update.data_operate_log(user, '[TeacherInfo]update: teacher_id:{} first_semester_expect {} second_semester_expect {} lock_state {}'.format(
            teacher_id,
            modify_0,
            modify_1,
            lock_state))
        status = 'Success'
    result = json.dumps({'status': status})
    return HttpResponse(result)


# @csrf_exempt
# def teacher_table_upload(request):
#     input_file = request.FILES.get("file_data", None)
#     work_book = xlrd.open_workbook(filename=None, file_contents=input_file.read())
#     # TODO: result part
#     work_sheet = work_book.sheet_by_name('教师列表')
#     line_length = work_sheet.nrows
#     teacher_list = []
#     line_width = work_sheet.row_len(0)
#     for line_number in range(line_length):
#
#         teacher_id, teacher_name, _ = work_sheet.row(line_number)
#         if type(teacher_id.value) == float:
#             teacher_list.append([str(int(teacher_id.value)), teacher_name.value])
#         else:
#             if teacher_id.value and teacher_id.value != '工号':
#                 teacher_list.append([teacher_id.value, teacher_name.value])
#     insert_teacher_list_into_db(teacher_list)
#     status = 'Pass'
#     result = json.dumps({'result': status})
#     return HttpResponse(result)


@csrf_exempt
def teacher_table_upload(request):
    input_file = request.FILES.get("file_data", None)
    work_book = xlrd.open_workbook(filename=None, file_contents=input_file.read())
    # TODO: result part
    work_sheet = work_book.sheet_by_name('教师信息')
    line_length = work_sheet.nrows
    teacher_list = []
    line_width = work_sheet.row_len(0)
    user = request.user.last_name + request.user.first_name + request.user.username
    for line_number in range(line_length):
        teacher_index = work_sheet.row(line_number)[0].value
        teacher_name = work_sheet.row(line_number)[2].value
        if type(teacher_index) == float and teacher_name:
            teacher_list.append(work_sheet.row(line_number))

    retCode = insert_teacher_extend_info_into_db(teacher_list, user)
    if retCode:
        status = 'Pass'
    else:
        status = 'Fail'
    result = json.dumps({'result': status})
    return HttpResponse(result)


@csrf_exempt
def teacher_help_declare_upload(request):
    # todo format not sure
    input_file = request.FILES.get("file_data", None)
    work_book = xlrd.open_workbook(filename=None, file_contents=input_file.read())
    # TODO: result part
    work_sheet = work_book.sheet_by_name('代理申报')
    user = request.user.last_name + request.user.first_name + request.user.username
    line_length = work_sheet.nrows
    teacher_list = []
    line_width = work_sheet.row_len(0)
    main_content = False
    for line_number in range(line_length):
        line_content = work_sheet.row(line_number)
        if line_content[0].value == '代码':
            main_content = True
            continue
        if main_content:
            search_result = CourseInfo.objects.filter(course_id=line_content[0].value)
            if search_result:
                suit_teacher_list = search_result[0].suit_teacher.split(',')
                teacher_ordered_list = search_result[0].teacher_ordered.split(',')
                if line_content[10].value not in suit_teacher_list:
                    suit_teacher_list.append(line_content[10].value)
                if line_content[10].value not in teacher_ordered_list:
                    teacher_ordered_list.append(line_content[10].value)
                suit_teacher_str = ','.join(suit_teacher_list)
                teacher_ordered_str = ','.join(teacher_ordered_list)
                CourseInfo.objects.filter(id=search_result[0].id).update(suit_teacher=suit_teacher_str, teacher_ordered=
                                                                         teacher_ordered_str)
                module_log_update.data_operate_log(user, '[CourseInfo]update: suit_teacher {} teacher_ordered {}'.format(suit_teacher_str, teacher_ordered_str))
    status = 'Pass'
    result = json.dumps({'result': status})
    return HttpResponse(result)


def insert_teacher_list_into_db(teacher_list, user=''):
    for eachTeacher in teacher_list:
        searchResult = TeacherInfo.objects.all().filter(teacher_id=eachTeacher[0])
        if searchResult:
            TeacherInfo.objects.filter(teacher_id=eachTeacher[0]).update(teacher_name=eachTeacher[1])
            module_log_update.data_operate_log(user, '[TeacherInfo]update: teacher_id {} teacher_name {}'.format(eachTeacher[0],eachTeacher[1]))
        else:
            TeacherInfo.objects.create(teacher_id=eachTeacher[0], teacher_name=eachTeacher[1], first_semester_expect=1.0, second_semester_expect=1.0)
            module_log_update.data_operate_log(user, '[TeacherInfo]create: teacher_id {} teacher_name {}'.format(eachTeacher[0],eachTeacher[1]))


def insert_teacher_extend_info_into_db(teacher_list, user=''):
    now = datetime.now()
    output = ""
    retCode = True
    for eachTeacher in teacher_list:
        teacher_name = eachTeacher[2].value
        major = eachTeacher[1].value
        teacher_id = eachTeacher[3].value
        if eachTeacher[4].value:
            birthday = xlrd.xldate.xldate_as_datetime(eachTeacher[4].value, 0)
        else:
            birthday = now
        teacher_title = eachTeacher[5].value
        teacher_type = eachTeacher[6].value
        sex = eachTeacher[7].value
        lock_state = 0
        if eachTeacher[8].value:
            if eachTeacher[8].value == '非激活':
                lock_state = 1
        searchResult = TeacherInfo.objects.all().filter(teacher_name=eachTeacher[2].value)
        if searchResult:
            TeacherInfo.objects.filter(teacher_name=eachTeacher[2].value).update(major=major,
                                                                                 birthday=birthday,
                                                                                 teacher_title=teacher_title,
                                                                                 teacher_type=teacher_type,
                                                                                 sex=sex,
                                                                                 lock_state=lock_state,
                                                                                 update_time=now)
            module_log_update.data_operate_log(user, '[TeacherInfo]update: teacher_name {} major: {} birthday: {} teacher_title: {} teacher_type: {} sex: {} lock_state{}'.format(
                eachTeacher[2].value,
                major,
                birthday,
                teacher_title,
                teacher_type,
                sex,
                lock_state))
        else:
            TeacherInfo.objects.create(teacher_name=teacher_name,
                                       teacher_id=teacher_id,
                                       major=major,
                                       birthday=birthday,
                                       teacher_title=teacher_title,
                                       teacher_type=teacher_type,
                                       sex=sex,
                                       first_semester_expect=1.0,
                                       second_semester_expect=1.0,
                                       lock_state=lock_state,
                                       update_time=now)
            module_log_update.data_operate_log(user, '[TeacherInfo]create: teacher_name: {} teacher_id: {} major: {} birthday: {} teacher_title: {} teacher_type: {} sex: {} lock_state{}'.format(
                teacher_name,
                teacher_id,
                major,
                birthday,
                teacher_title,
                teacher_type,
                sex,
                lock_state))

    return retCode

def save_teacher_to_course_info(course_id, user_name, user=''):
    course_id_current = course_id.split('/')[0]
    search_result = CourseInfo.objects.all().filter(course_id=course_id_current)
    if search_result:

        teacher_list = search_result[0].teacher_ordered.split(',')
        if len(teacher_list) == 1 and teacher_list[0] == '':
            teacher_str = user_name
        else:
            if user_name not in teacher_list:
                teacher_list.append(user_name)
            teacher_str = ','.join(teacher_list)
        CourseInfo.objects.filter(course_id=course_id_current).update(teacher_ordered=teacher_str, suit_teacher=teacher_str)
        module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} teacher_ordered {} suit_teacher {}'.format(course_id, teacher_str, teacher_str))
        if search_result[0].course_relate:
            course_relate_list = search_result[0].course_relate.split(',')
            for each_relate_course in course_relate_list:
                CourseInfo.objects.filter(course_id=each_relate_course).update(teacher_ordered=teacher_str,
                                                                      suit_teacher=teacher_str)
                module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} teacher_ordered {} suit_teacher {}'.format(course_id, teacher_str, teacher_str))
    return 'Success'


def remove_teacher_from_course_info(course_id, user_name, user=''):
    course_id_current = course_id.split('/')[0]
    search_result = CourseInfo.objects.all().filter(course_id=course_id_current)
    status = 'Success'
    if search_result:
        teacher_list = search_result[0].teacher_ordered.split(',')
        if len(teacher_list) == 0:
            status = '你并未申报此课程, 取消失败'
            return status
        else:
            if user_name in teacher_list:
                teacher_list.remove(user_name)
            else:
                status = '你并未申报此课程, 取消失败'
            teacher_str = ','.join(teacher_list)
        CourseInfo.objects.filter(course_id=course_id_current).update(teacher_ordered=teacher_str, suit_teacher=teacher_str)
        module_log_update.data_operate_log(user,
                                           '[CourseInfo]update: course_id {} teacher_ordered {} suit_teacher {}'.format(course_id_current, teacher_str, teacher_str))
        if search_result[0].course_relate:
            course_relate_list = search_result[0].course_relate.split(',')
            for each_relate_course in course_relate_list:
                CourseInfo.objects.filter(course_id=each_relate_course).update(teacher_ordered=teacher_str,
                                                                      suit_teacher=teacher_str)
                module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} teacher_ordered {} suit_teacher {}'.format(each_relate_course,
                                                                                               teacher_str,
                                                                                               teacher_str))
    return status


@csrf_exempt
def teacher_submit_apply_status(request):
    status_code = request.POST['status']
    teacher_id = request.POST['teacher_id']
    search_result = TeacherInfo.objects.filter(teacher_id=teacher_id, lock_state=0)
    user = request.user.last_name + request.user.first_name + request.user.username
    if search_result:
        teacher_name = search_result[0].teacher_name
    else:
        result = json.dumps({'status': '该老师没有在系统中注册'})
        return HttpResponse(result)
    if status_code == 'check':
        notes = TeacherInfo.objects.filter(teacher_id=teacher_id).values('notes')[0]['notes']
        search_result = CourseInfo.objects.filter(lock_state=0)
        result_teacher = {STUDENT_TYPE[0]: [], STUDENT_TYPE[1]: [], STUDENT_TYPE[2]: [], STUDENT_TYPE[3]: []}
        for eachCourse in search_result:
            if eachCourse.course_relate and eachCourse.student_type != '本科':
                continue
            teacher_list = eachCourse.teacher_ordered.split(',')
            if teacher_name in teacher_list:
                tmp = [eachCourse.course_id, eachCourse.course_name, eachCourse.course_degree]
                result_teacher[eachCourse.student_type].append(tmp)
        # print result_teacher
        status = 'Success'
        result = json.dumps({'status': status, 'list_1': result_teacher[STUDENT_TYPE[0]], 'list_2': result_teacher[STUDENT_TYPE[1]],
                             'list_3': result_teacher[STUDENT_TYPE[2]], 'list_4': result_teacher[STUDENT_TYPE[3]],'notes':notes})
    elif status_code == 'save':
        status = 'Success'
        notes = request.POST['notes']
        if notes[:6] == '满足申报要求':
            TeacherInfo.objects.filter(teacher_id=teacher_id).update(teacher_apply_done='申报结束', notes=notes[6:])
            module_log_update.data_operate_log(user, '[TeacherInfo] teacher_id: {} teacher_apply_done: {} notes: {}'.format(
                teacher_id,
                '申报结束',
                notes[6:]
            ))
        elif notes[:7] == '不满足申报要求':
            TeacherInfo.objects.filter(teacher_id=teacher_id).update(teacher_apply_done='申报结束/不满足申报要求', notes=notes[7:])
            module_log_update.data_operate_log(user, '[TeacherInfo] teacher_id: {} teacher_apply_done: {} notes: {}'.format(
                teacher_id,
                '申报结束/不满足申报要求',
                notes[7:]
            ))
        else:
            status = '申报状态出错，{}'.format(notes)
        result = json.dumps({'status': status})
    elif status_code == 'recall':
        status = 'Success'
        TeacherInfo.objects.filter(teacher_id=teacher_id).update(teacher_apply_done='申报结束/申请撤回申报完成')
        module_log_update.data_operate_log(user, '[TeacherInfo] teacher_id: {} teacher_apply_done: {}'.format(
            teacher_id,
            '申报结束/不满足申报要求',
        ))
        result = json.dumps({'status': status})
    elif status_code == 'approve':
        if search_result[0].teacher_apply_done == '申报结束/申请撤回申报完成':
            status = 'Success'
            TeacherInfo.objects.filter(teacher_id=teacher_id).update(teacher_apply_done='')
            module_log_update.data_operate_log(user, '[TeacherInfo] teacher_id: {} teacher_apply_done: {}'.format(
                teacher_id,
                '',
            ))
        else:
            status = '该教师无撤销申报的申请'
        result = json.dumps({'status': status})
    else:
        status = 'Unknown status code {}'.format(status_code)
        result = json.dumps({'status': status})
    return HttpResponse(result)

@csrf_exempt
def check_teacher_apply_status(request):
    course_table = CourseInfo.objects.filter(lock_state=0)
    final_result = {'status': 'Success', 'message':[]}
    for eachCourse in course_table:
        teacher_limit_basic = eachCourse.allow_teachers

        if eachCourse.course_parallel and int(eachCourse.course_parallel) != 1:
            teacher_limit_final = teacher_limit_basic * int(eachCourse.course_parallel)
        else:
            teacher_limit_final = teacher_limit_basic
        teacher_list = eachCourse.teacher_ordered.split(',')
        teacher_count = len(teacher_list) if teacher_list else 0
        if teacher_count < teacher_limit_final and teacher_count >= teacher_limit_basic:
            notes = '{} {} 申报教师数满足授课最低要求,但是需要某些教师授课多次{}'.format(eachCourse.course_id,eachCourse.course_name,os.linesep)
            final_result['message'].append(notes)
        elif teacher_count < teacher_limit_basic:
            notes = '{} {} 申报教师不满足授课最低要求{}'.format(eachCourse.course_id,eachCourse.course_name,os.linesep)
            final_result['message'].append(notes)
        else:
            pass
    if len(final_result['message']) == 0:
        final_result['message'] = ['所有课程的申报教师数均符合要求']
    result = json.dumps({'status': final_result['status'], 'message': final_result['message']})
    return HttpResponse(result)

def get_teacher_final_pick(final_pick, teacher_order):
    if final_pick:
        final_pick_list = final_pick.split(',')
        tmp_list = []
        for eachTeacher in final_pick_list:
            if eachTeacher in teacher_order.split(','):
                tmp_list.append(eachTeacher)
            else:
                tmp_list.append("{}(未申报)".format(eachTeacher))
        tmp_str = ','.join(tmp_list)
        return tmp_str
    else:
        return ''


@login_required()
def class_manage(request):
    search_result = CurrentStepInfo.objects.all()
    if search_result:
        current_year = search_result[0].s1_year_info
    else:
        current_year = 'None'
    search_result_major = CourseInfo.objects.values('major')
    major_list = []
    for row_major in search_result_major:
        if row_major['major']:
            if row_major['major'] == '综合':
                major_list.insert(0, row_major['major'])
            else:
                major_list.append(row_major['major'])

    major_list_temp = []
    for eachItem in major_list:
        if eachItem not in major_list_temp:
            major_list_temp.append(eachItem)

    course_table = CourseInfo.objects.all().filter()
    search_result = []

    class_name = get_class_value_by_key('class_name')#CLASS_NAME_LIST
    student_type = get_class_value_by_key('student_type')#STUDENT_TYPE
    year = get_class_value_by_key('year')#CLASS_GRADE
    semester = SEMESTER
    course_hour = COURSE_HOUR
    course_degree = COURSE_DEGREE
    course_type = get_class_value_by_key('course_type')#COURSE_TYPE
    current_course_count = len(course_table)
    current_hour_count = 0
    current_degree_count = 0
    current_course_claim = 0
    lock_class_count = 0
    unlock_class_count = 0
    course_relate_dict = {}
    for eachItem in course_table:
        if eachItem.lock_state == 1:
            lock_state = '非激活'
            if eachItem.course_relate and eachItem.student_type != '本科':
                lock_class_count += 0
            else:
                lock_class_count += 1
        else:
            lock_state = ''

            tmp_hour, tmp_degree = get_course_effective_point(eachItem)
            tmp_course_count, tmp_claim_count = get_course_effective_count(eachItem)
            unlock_class_count += tmp_course_count
            current_hour_count += tmp_hour
            current_degree_count += tmp_degree
            current_course_claim += tmp_claim_count
        if not eachItem.class_name:
            continue
        for eachClass in eachItem.class_name.split(' '):
            tmp_student = eachClass.split('-')[0]
            tmp_class_grade, tmp_class_name = eachClass.split('-')[-1].split('_')
            if eachItem.course_relate:
                course_relate = eachItem.course_relate.strip(',')
            else:
                course_relate = ''
            teacher_final_pick_str = get_teacher_final_pick(eachItem.teacher_final_pick, eachItem.teacher_ordered)
            search_result.append([eachItem.course_id,
                                  eachItem.course_name,
                                  eachItem.major,
                                  tmp_student,
                                  tmp_class_grade,
                                  tmp_class_name,
                                  eachItem.semester,
                                  eachItem.course_hour,
                                  eachItem.course_degree,
                                  eachItem.course_type,
                                  eachItem.language,
                                  eachItem.allow_teachers,
                                  eachItem.times_every_week,
                                  eachItem.teacher_ordered,
                                  course_relate,
                                  get_excellent_course(eachItem.excellent_course),
                                  lock_state,
                                  eachItem.course_parallel,
                                  teacher_final_pick_str,
                                  eachItem.notes if eachItem.notes else ''])
        # if eachItem.lock_state == 0:
        #     tmp_hour, tmp_degree = get_course_effective_point(eachItem)
        #     current_hour_count += tmp_hour
        #     current_degree_count += tmp_degree
        #     if eachItem.suit_teacher:
        #         current_course_claim += 1
    summary_table = [unlock_class_count, current_hour_count, current_degree_count, current_course_claim, lock_class_count]

    table_head = ['代码', '名称', '专业', '学位', '年级', '班级', '学期', '学时', '难度', '必/选', '语言', '教师数', '周上课次数', '申报教师', '打通课程代码','是否精品课程','状态','平行班级数','授课教师','备注']
    table_default = ['',
                     '',
                     major_list_temp,
                     student_type,
                     year,
                     class_name,
                     semester,
                     course_hour,
                     course_degree,
                     course_type,
                     LANGUAGE,
                     '',
                     '',
                     '',
                     '',
                     ['非精品课程','校级精品课程','上海市精品课程','国家级精品开放课程'],
                     ['激活','非激活']]
    return render(request, 'class_manage.html', {'UserName': request.user.last_name+request.user.first_name+request.user.username, 'class_table': search_result,
                                                 'table_head': table_head, 'table_default': table_default,
                                                 'summary_table': summary_table, 'year': current_year, 'major': major_list_temp})


def get_class_value_by_key(key):
    if key in ['class_name', 'year', 'student_type']:
        searchKey = 'class_name'
    else:
        searchKey = key
    search_result_key = CourseInfo.objects.values(searchKey)
    class_value_list = []
    for row_item in search_result_key:
        if row_item[searchKey]:
            if key == 'class_name':
                tmp_value = row_item[searchKey].split('_')[-1]
            elif key == 'year':
                tmp_value = row_item[searchKey].split('_')[0].split('-')[-1]
                if not tmp_value:
                    continue
            elif key == 'student_type':
                tmp_value = row_item[searchKey].split('_')[0].split('-')[0]
            else:
                tmp_value = row_item[searchKey]
            if tmp_value not in class_value_list:
                class_value_list.append(tmp_value)
    return class_value_list


def get_course_effective_count(course_object):
    unlock_course_count = 0
    claim_teacher_count = 0
    if course_object.course_relate:
        if course_object.student_type == '本科':
            unlock_course_count = 1
            if course_object.teacher_ordered:
                claim_teacher_count = 1
    else:
        unlock_course_count = 1
        if course_object.teacher_ordered:
            claim_teacher_count = 1
    return unlock_course_count, claim_teacher_count


def get_course_effective_point(course_object):
    if course_object.course_relate:
        if course_object.student_type == '本科':
            return float(course_object.course_hour), float(course_object.course_degree)
        else:
            return 0, 0
    else:
        if course_object.course_parallel:
            return float(course_object.course_hour)*int(course_object.course_parallel), float(course_object.course_degree)*int(course_object.course_parallel)
        else:
            return float(course_object.course_hour), float(course_object.course_degree)


@csrf_exempt
def class_filter_by_submit(request):
    student_type = request.POST['type'].strip().split(' ')
    semester = request.POST['semester'].strip().split(' ')
    table_id = request.POST['table_id']
    major_list = json.loads(request.POST['major_list'])
    course_table = CourseInfo.objects.filter()
    search_result = []
    for eachItem in course_table:
        if eachItem.semester in semester and eachItem.student_type in student_type:
            if eachItem.major and eachItem.major in major_list:
                if table_id == 'table_course_manage':
                    for eachClass in eachItem.class_name.split(' '):
                        if eachItem.lock_state == 1:
                            lock_state = '非激活'
                        else:
                            lock_state = ''
                        teacher_final_pick_str = get_teacher_final_pick(eachItem.teacher_final_pick,
                                                                        eachItem.teacher_ordered)
                        search_result.append([eachItem.course_id,
                                              eachItem.course_name,
                                              eachItem.major,
                                              eachItem.student_type,
                                              eachClass.split('-')[-1].split('_')[0],
                                              eachClass.split('-')[-1].split('_')[-1],
                                              eachItem.semester,
                                              eachItem.course_hour,
                                              eachItem.course_degree,
                                              eachItem.course_type,
                                              eachItem.language,
                                              eachItem.allow_teachers,
                                              eachItem.times_every_week,
                                              eachItem.teacher_ordered,
                                              eachItem.course_relate,
                                              get_excellent_course(eachItem.excellent_course),
                                              lock_state,
                                              eachItem.course_parallel,
                                              teacher_final_pick_str,
                                              eachItem.notes if eachItem.notes else ''])
                elif table_id == 'table_course_personal':
                    if eachItem.lock_state == 1:
                        continue
                    teacher_list = eachItem.teacher_ordered.split(',') if eachItem.teacher_ordered else []
                    if request.user.last_name + request.user.first_name in teacher_list \
                            and request.user.last_name + request.user.first_name != '':
                        tmp = '已申报'
                    else:
                        tmp = ''
                    if eachItem.course_relate and eachItem.student_type != '本科':
                        continue
                    class_name_list = eachItem.class_name.split(' ')
                    if eachItem.course_relate and eachItem.student_type == '本科':
                        course_relate_list = eachItem.course_relate.split(',')
                        for eachCourseId in course_relate_list:
                            if CourseInfo.objects.filter(course_id=eachCourseId):
                                class_name_list.extend(CourseInfo.objects.filter(course_id=eachCourseId)[0].class_name.split(' '))
                    # class_name_str = ' '.join(class_name_list)
                    # class_name_str = ' / '.join((' '.join(class_name_list)).split(' '))
                    class_name_str = get_class_name(class_name_list)
                    if eachItem.course_relate:
                        course_relate = eachItem.course_relate.strip(',')
                        course_id_str = '{} / {}'.format(eachItem.course_id, course_relate)
                        student_type_relate = CourseInfo.objects.filter(course_id=course_relate)[0].student_type
                        student_type_str = '{} / {}'.format(eachItem.student_type, student_type_relate)
                    else:
                        course_id_str = eachItem.course_id
                        student_type_str = eachItem.student_type
                    # search_result.append([eachItem.course_id,
                    #                       eachItem.course_name,
                    #                       eachItem.major,
                    #                       eachItem.student_type,
                    #                       class_name_str,
                    #                       eachItem.semester,
                    #                       eachItem.course_hour,
                    #                       eachItem.course_degree,
                    #                       eachItem.course_type,
                    #                       eachItem.language,
                    #                       eachItem.allow_teachers,
                    #                       eachItem.times_every_week,
                    #                       eachItem.course_relate,
                    #                       eachItem.course_parallel,
                    #                       eachItem.excellent_course,
                    #                       tmp])
                    search_result.append([course_id_str,
                                          eachItem.course_name,
                                          eachItem.major,
                                          student_type_str,
                                          class_name_str,
                                          eachItem.semester,
                                          eachItem.course_hour,
                                          eachItem.course_degree,
                                          eachItem.course_type,
                                          eachItem.language,
                                          eachItem.allow_teachers,
                                          eachItem.times_every_week,
                                          eachItem.course_parallel,
                                          get_excellent_course(eachItem.excellent_course),
                                          tmp])
    result = json.dumps({'result': search_result})
    return HttpResponse(result)


@csrf_exempt
def class_save_one_row(request):
    user = request.user.last_name + request.user.first_name + request.user.username
    course_info = json.loads(request.POST['row_data'])
    # in case of wrong course lock state input
    # lock_state_position = -3
    # if not course_info[lock_state_position]:
    #     course_info[lock_state_position] = 0
    # else:
    #     if int(course_info[lock_state_position]) != 1:
    #         course_info[lock_state_position] = 0
    old_class_info = request.POST['old_data']
    if 'old_course_id' in request.POST:
        old_course_id = request.POST['old_course_id']
        save_course_into_database_by_edit(course_info, old_class_info, old_course_id, user)
    else:
        save_course_into_database_by_add(course_info, old_class_info, user)
    result = 'Success'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def save_course_into_database_by_edit(course_info, old_class_info, old_course_id=None,user=''):
    now = datetime.now()
    search_result = CourseInfo.objects.all().filter(course_id=course_info[0])
    allow_teachers = course_info[11]
    course_parallel = course_info[17]
    lock_state = course_info[16]
    if lock_state == '非激活':
        lock_state = 1
    else:
        lock_state = 0
    excellent_course = course_info[15]
    # if excellent_course != '精品课程':
    #     excellent_course = '非精品课程'
    excellent_course = get_excellent_course(excellent_course)
    if search_result:
        combine_class_name = '{}-{}_{}'.format(course_info[3], course_info[4], course_info[5])
        if combine_class_name in search_result[0].class_name:
            CourseInfo.objects.filter(id=search_result[0].id).update(course_id=course_info[0],
                                                                     course_name=course_info[1],
                                                                     major=course_info[2],
                                                                     semester=course_info[6],
                                                                     course_hour=course_info[7],
                                                                     course_degree=course_info[8],
                                                                     course_type=course_info[9],
                                                                     language=course_info[10],
                                                                     allow_teachers=allow_teachers,
                                                                     times_every_week=course_info[12],
                                                                     suit_teacher=course_info[13],
                                                                     course_relate=course_info[14],
                                                                     excellent_course=excellent_course,
                                                                     lock_state=lock_state,
                                                                     course_parallel=course_parallel,
                                                                     notes=course_info[19],
                                                                     update_time=now)
            module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} course_name {} major {} semester {} course_hour {} course_degree {} course_type {} language {} allow_teachers {} times_every_week {} suit_teacher {} course_relate {} excellent_course {} lock_state {} course_parallel {} notes {}'.format(
                course_info[0],
                course_info[1],
                course_info[2],
                course_info[6],
                course_info[7],
                course_info[8],
                course_info[9],
                course_info[10],
                allow_teachers,
                course_info[12],
                course_info[13],
                course_info[14],
                excellent_course,
                lock_state,
                course_parallel,
                course_info[19],
            ))
        else:
            class_list = search_result[0].class_name.split(' ')
            if old_class_info:
                if old_class_info in class_list:
                    class_list.remove(old_class_info)
                suit_teacher = course_info[13]
            else:
                suit_teacher = search_result[0].suit_teacher

            class_list.append(combine_class_name)
            class_name_str = ' '.join(class_list)
            CourseInfo.objects.filter(id=search_result[0].id).update(course_id=course_info[0],
                                                                     course_name=course_info[1],
                                                                     major=course_info[2],
                                                                     class_name=class_name_str,
                                                                     semester=course_info[6],
                                                                     course_hour=course_info[7],
                                                                     course_degree=course_info[8],
                                                                     course_type=course_info[9],
                                                                     language=course_info[10],
                                                                     allow_teachers=allow_teachers,
                                                                     times_every_week=course_info[12],
                                                                     suit_teacher=suit_teacher,
                                                                     course_relate=course_info[14],
                                                                     excellent_course=excellent_course,
                                                                     lock_state=lock_state,
                                                                     course_parallel=course_parallel,
                                                                     notes=course_info[19],
                                                                     update_time=now)
            module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} course_name {} major {} class_name {} semester {} course_hour {} course_degree {} course_type {} language {} allow_teachers {} times_every_week {} suit_teacher {} course_relate {} excellent_course {} lock_state {} course_parallel {} notes {}'.format(
                course_info[0],
                course_info[1],
                course_info[2],
                class_name_str,
                course_info[6],
                course_info[7],
                course_info[8],
                course_info[9],
                course_info[10],
                allow_teachers,
                course_info[12],
                suit_teacher,
                course_info[14],
                excellent_course,
                lock_state,
                course_parallel,
                course_info[19],
            ))
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
                module_log_update.data_operate_log(user, '[CourseInfo]delete: course_id {}'.format(old_course_id))
            else:
                class_name_str = ' '.join(class_list)
                CourseInfo.objects.filter(course_id=old_course_id).update(class_name=class_name_str)
                module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} class_name {}'.format(old_course_id, class_name_str))
        # add a new course
        combine_class_name = '{}-{}_{}'.format(course_info[3], course_info[4], course_info[5])
        CourseInfo.objects.create(course_id=course_info[0],
                                  course_name=course_info[1],
                                  major=course_info[2],
                                  student_type=course_info[3],
                                  year=current_school_year,
                                  class_name=combine_class_name,
                                  semester=course_info[6],
                                  course_hour=course_info[7],
                                  course_degree=course_info[8],
                                  course_type=course_info[9],
                                  language=course_info[10],
                                  allow_teachers=allow_teachers,
                                  times_every_week=course_info[12],
                                  suit_teacher='',
                                  teacher_ordered='',
                                  course_relate=course_info[14],
                                  excellent_course=excellent_course,
                                  lock_state=lock_state,
                                  course_parallel=course_parallel,
                                  notes=course_info[19],
                                  update_time=now)
        module_log_update.data_operate_log(user,
                                           '[CourseInfo]create: course_id {} course_name {} major {} student_type {} year {} class_name {} semester {} course_hour {} course_degree {} course_type {} language {} allow_teachers {} times_every_week {} suit_teacher {} teacher_ordered {} course_relate {} excellent_course {} lock_state {} course_parallel {} notes {}'.format(
                                               course_info[0],
                                               course_info[1],
                                               course_info[2],
                                               course_info[3],
                                               current_school_year,
                                               combine_class_name,
                                               course_info[6],
                                               course_info[7],
                                               course_info[8],
                                               course_info[9],
                                               course_info[10],
                                               allow_teachers,
                                               course_info[12],
                                               '',
                                               '',
                                               course_info[14],
                                               excellent_course,
                                               lock_state,
                                               course_parallel,
                                               course_info[19],
                                           ))


def save_course_into_database_by_add(course_info, old_class_info, user=''):
    now = datetime.now()
    search_result = CourseInfo.objects.all().filter(course_id=course_info[0])
    allow_teachers = course_info[11]
    course_parallel = course_info[17]
    lock_state = course_info[16]
    if lock_state == '非激活':
        lock_state = 1
    else:
        lock_state = 0
    excellent_course = course_info[15]
    # if excellent_course != '精品课程':
    #     excellent_course = '非精品课程'
    excellent_course = get_excellent_course(excellent_course)
    if search_result:
        combine_class_name = '{}-{}_{}'.format(course_info[3], course_info[4], course_info[5])
        if combine_class_name in search_result[0].class_name:
            CourseInfo.objects.filter(id=search_result[0].id).update(course_id=course_info[0],
                                                                     course_name=course_info[1],
                                                                     major=course_info[2],
                                                                     semester=course_info[6],
                                                                     course_hour=course_info[7],
                                                                     course_degree=course_info[8],
                                                                     course_type=course_info[9],
                                                                     language=course_info[10],
                                                                     allow_teachers=allow_teachers,
                                                                     times_every_week=course_info[12],
                                                                     # suit_teacher=course_info[11],
                                                                     course_relate=course_info[14],
                                                                     excellent_course=excellent_course,
                                                                     lock_state=lock_state,
                                                                     course_parallel=course_parallel,
                                                                     notes=course_info[19],
                                                                     update_time=now)
            module_log_update.data_operate_log(user,
                                               '[CourseInfo]update: course_id {} course_name {} major {} semester {} course_hour {} course_degree {} course_type {} language {} allow_teachers {} times_every_week {} course_relate {} excellent_course {} lock_state {} course_parallel {} notes {}'.format(
                                                   course_info[0],
                                                   course_info[1],
                                                   course_info[2],
                                                   course_info[6],
                                                   course_info[7],
                                                   course_info[8],
                                                   course_info[9],
                                                   course_info[10],
                                                   allow_teachers,
                                                   course_info[12],
                                                   course_info[14],
                                                   excellent_course,
                                                   lock_state,
                                                   course_parallel,
                                                   course_info[19],
                                               ))
        else:
            class_list = search_result[0].class_name.split(' ')
            class_list.append(combine_class_name)
            if old_class_info:
                class_list.remove(old_class_info)
                suit_teacher = course_info[13]
            else:
                suit_teacher = search_result[0].suit_teacher
            class_name_str = ' '.join(class_list)
            CourseInfo.objects.filter(id=search_result[0].id).update(course_id=course_info[0],
                                                                     course_name=course_info[1],
                                                                     major=course_info[2],
                                                                     class_name=class_name_str,
                                                                     semester=course_info[6],
                                                                     course_hour=course_info[7],
                                                                     course_degree=course_info[8],
                                                                     course_type=course_info[9],
                                                                     language=course_info[10],
                                                                     allow_teachers=allow_teachers,
                                                                     times_every_week=course_info[12],
                                                                     # suit_teacher=suit_teacher,
                                                                     course_relate=course_info[14],
                                                                     excellent_course=excellent_course,
                                                                     lock_state=lock_state,
                                                                     course_parallel=course_parallel,
                                                                     notes=course_info[19],
                                                                     update_time=now)
            module_log_update.data_operate_log(user,
                                               '[CourseInfo]update: course_id {} course_name {} major {} class_name {} semester {} course_hour {} course_degree {} course_type {} language {} allow_teachers {} times_every_week {} course_relate {} excellent_course {} lock_state {} course_parallel {} notes {}'.format(
                                                   course_info[0],
                                                   course_info[1],
                                                   course_info[2],
                                                   class_name_str,
                                                   course_info[6],
                                                   course_info[7],
                                                   course_info[8],
                                                   course_info[9],
                                                   course_info[10],
                                                   allow_teachers,
                                                   course_info[12],
                                                   course_info[14],
                                                   excellent_course,
                                                   lock_state,
                                                   course_parallel,
                                                   course_info[19],
                                               ))
    else:
        combine_class_name = '{}-{}_{}'.format(course_info[3], course_info[4], course_info[5])
        CourseInfo.objects.create(course_id=course_info[0],
                                  course_name=course_info[1],
                                  major=course_info[2],
                                  student_type=course_info[3],
                                  year=current_school_year,
                                  class_name=combine_class_name,
                                  semester=course_info[6],
                                  course_hour=course_info[7],
                                  course_degree=course_info[8],
                                  course_type=course_info[9],
                                  language=course_info[10],
                                  allow_teachers=allow_teachers,
                                  times_every_week=course_info[12],
                                  suit_teacher='',
                                  teacher_ordered='',
                                  course_relate=course_info[14],
                                  excellent_course=excellent_course,
                                  lock_state=lock_state,
                                  course_parallel=course_parallel,
                                  notes=course_info[19],
                                  update_time=now)
        module_log_update.data_operate_log(user,
                                           '[CourseInfo]create: course_id {} course_name {} major {} student_type {} year {} class_name {} semester {} course_hour {} course_degree {} course_type {} language {} allow_teachers {} times_every_week {} suit_teacher {} teacher_ordered {} course_relate {} excellent_course {} lock_state {} course_parallel {} notes {}'.format(
                                               course_info[0],
                                               course_info[1],
                                               course_info[2],
                                               course_info[3],
                                               current_school_year,
                                               combine_class_name,
                                               course_info[6],
                                               course_info[7],
                                               course_info[8],
                                               course_info[9],
                                               course_info[10],
                                               allow_teachers,
                                               course_info[12],
                                               '',
                                               '',
                                               course_info[14],
                                               excellent_course,
                                               lock_state,
                                               course_parallel,
                                               course_info[19],
                                           ))


# temp use
def save_course_into_database(course_info):
    now = datetime.now()
    search_result = CourseInfo.objects.all().filter(course_id=course_info[0])
    # print course_info
    if search_result:
        CourseInfo.objects.filter(id=search_result[0].id).update(course_id=course_info[0],
                                                                 course_name=course_info[1],
                                                                 student_type=course_info[2],
                                                                 year=course_info[3],
                                                                 class_name=course_info[4],
                                                                 semester=course_info[5],
                                                                 course_hour=course_info[6],
                                                                 course_degree=course_info[7],
                                                                 course_type=course_info[8],
                                                                 allow_teachers=course_info[9],
                                                                 times_every_week=course_info[10],
                                                                 suit_teacher=course_info[11],
                                                                 teacher_ordered=course_info[12],
                                                                 excellent_course=course_info[13],
                                                                 major=course_info[14],
                                                                 language=course_info[15],
                                                                 course_relate=course_info[16],
                                                                 lock_state=course_info[17],
                                                                 course_parallel=course_info[18],
                                                                 update_time=now)
    else:
        CourseInfo.objects.create(course_id=course_info[0],
                                  course_name=course_info[1],
                                  student_type=course_info[2],
                                  year=course_info[3],
                                  class_name=course_info[4],
                                  semester=course_info[5],
                                  course_hour=course_info[6],
                                  course_degree=course_info[7],
                                  course_type=course_info[8],
                                  allow_teachers=course_info[9],
                                  times_every_week=course_info[10],
                                  suit_teacher=course_info[11],
                                  teacher_ordered=course_info[12],
                                  excellent_course=course_info[13],
                                  major=course_info[14],
                                  language=course_info[15],
                                  course_relate=course_info[16],
                                  lock_state=course_info[17],
                                  course_parallel=course_info[18],
                                  update_time=now)


@csrf_exempt
def class_delete_one_row(request):
    course_id = request.POST['course_id']
    old_class_info = request.POST['old_data']
    user = request.user.last_name + request.user.first_name + request.user.username
    delete_course_from_database(course_id, old_class_info, user)
    # TODO: result part
    result = 'Pass'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def delete_course_from_database(course_id, old_class_info, user=''):
    search_result = CourseInfo.objects.all().filter(course_id=course_id)
    if search_result:
        if len(search_result[0].class_name.split(' ')) > 1:
            class_list = search_result[0].class_name.split(' ')
            class_list.remove(old_class_info)
            class_name_str = ' '.join(class_list)
            CourseInfo.objects.filter(course_id=course_id).update(class_name=class_name_str)
            module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} class_name {}'.format(course_id, class_name_str))
        else:
            CourseInfo.objects.filter(course_id=course_id).delete()
            module_log_update.data_operate_log(user, '[CourseInfo]delete: {}'.format(course_id))
    else:
        return False


@csrf_exempt
def class_get_suit_teacher(request):
    course_id = request.POST['course_id']
    search_result = CourseInfo.objects.filter(course_id=course_id)
    if search_result:
        teacher_list = search_result[0].teacher_ordered.split(',')
    result_list = []
    for eachTeacher in teacher_list:
        search_result = TeacherInfo.objects.filter(teacher_name=eachTeacher)
        if search_result:
            tmp = [search_result[0].teacher_id, eachTeacher]
            result_list.append(tmp)
    class_name = get_class_value_by_key('class_name')#CLASS_NAME_LIST
    student_type = get_class_value_by_key('student_type')#STUDENT_TYPE
    year = get_class_value_by_key('year')#CLASS_GRADE
    semester = SEMESTER
    course_hour = COURSE_HOUR
    course_degree = COURSE_DEGREE
    course_type = get_class_value_by_key('course_type')#COURSE_TYPE
    info_default = [class_name, student_type, year, semester, course_hour, course_degree, course_type]
    result = json.dumps({'result_list': result_list, 'info_default':info_default})
    return HttpResponse(result)


# @csrf_exempt
# def class_table_upload(request):
#     input_file = request.FILES.get("file_data", None)
#     work_book = xlrd.open_workbook(filename=None, file_contents=input_file.read())
#     # TODO: result part
#     work_sheet = work_book.sheet_by_name('课程信息')
#     line_length = work_sheet.nrows
#     line_content = []
#     for line_number in range(line_length):
#         if line_number == 0:
#             continue
#         line_content.append(work_sheet.row(line_number))
#     class_info_to_save = []
#     for eachLine in line_content:
#
#         course_id = eachLine[7].value
#         course_name = eachLine[8].value
#         student_type = eachLine[3].value
#         year = eachLine[1].value
#         class_name = '{}-{}_{}'.format(student_type, int(eachLine[4].value) if eachLine[4].value else '', eachLine[5].value)
#         semester = eachLine[2].value
#         course_hour = eachLine[10].value
#         course_degree = eachLine[11].value
#         course_type = eachLine[12].value
#         allow_teachers = eachLine[14].value
#         times_every_week = eachLine[16].value
#         suit_teacher = eachLine[17].value
#         teacher_ordered = eachLine[17].value
#         notes = str(eachLine[22].value) if len(eachLine) >= 23 else ''
#         major = eachLine[23]
#         language = eachLine[24]
#         course_relate = eachLine[25]
#         class_info_to_save.append([course_id, course_name, student_type, year, class_name, semester, course_hour,
#                                    course_degree, course_type, allow_teachers, times_every_week, suit_teacher, teacher_ordered, notes,
#                                    major, language, course_relate])
#
#     save_course_table_into_database(class_info_to_save)
#     result = 'Pass'
#     result = json.dumps({'result': result})
#     return HttpResponse(result)


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
        print eachLine
        major = eachLine[5].value
        course_id = eachLine[6].value
        course_name = eachLine[7].value
        student_type = eachLine[2].value
        year = eachLine[0].value
        class_name = '{}-{}_{}'.format(student_type, int(eachLine[3].value) if eachLine[3].value else '',
                                       eachLine[4].value)
        # class_name = eachLine[5].value
        semester = eachLine[1].value
        course_hour = eachLine[9].value
        if not eachLine[10].value:
            course_degree = 0
        else:
            course_degree = eachLine[10].value
        course_type = eachLine[11].value
        if not eachLine[13].value:
            allow_teachers = 0
        else:
            allow_teachers = int(eachLine[13].value)
        if not eachLine[14].value:
            times_every_week = 0
        else:
            times_every_week = int(eachLine[14].value)
        suit_teacher = eachLine[15].value
        teacher_ordered = eachLine[15].value
        language = eachLine[12].value
        course_relate = eachLine[16].value
        if eachLine[19].value and eachLine[19].value == '非激活':
            lock_state = 1
        else:
            lock_state = 0
        course_parallel = int(eachLine[18].value) if eachLine[18].value else 1
        if eachLine[17].value:
            excellent_course = get_excellent_course(eachLine[17].value)
        else:
            excellent_course = ''

        class_info_to_save.append([course_id, course_name, student_type, year, class_name, semester, course_hour,
                                   course_degree, course_type, allow_teachers, times_every_week, suit_teacher,
                                   teacher_ordered, excellent_course, major, language, course_relate, lock_state,course_parallel])

    retCode = save_course_table_into_database(class_info_to_save)
    if retCode:
        result = 'Pass'
    else:
        result = 'Fail'
    result = json.dumps({'result': result})
    return HttpResponse(result)


def save_course_table_into_database(class_info_to_save):
    course_dict = {}
    output = ""
    retCode = True
    for rowNumber, eachCourse in enumerate(class_info_to_save):
        if eachCourse[0] not in course_dict.keys():
            course_dict[eachCourse[0]] = eachCourse
        else:
            if course_dict[eachCourse[0]][5] != eachCourse[5]:
                output += "行号：{} 课程：{}, 学期信息与相同课程号发生冲突\n".format(rowNumber+1, eachCourse)
                module_log_update.log_info('course_table', "行号：{} 课程：{}, 学期信息与相同课程号发生冲突\n".format(rowNumber+1, eachCourse))
            # elif eachCourse[4].split('_')[0] not in course_dict[eachCourse[0]][4]:
            #     output += "{}, 班级信息与相同课程号发生冲突\n".format(eachCourse)
                retCode = False
            else:
                course_dict[eachCourse[0]][4] += ' {}'.format(eachCourse[4])

    for tmpKey in course_dict.keys():
        each_course = course_dict[tmpKey]
        save_course_into_database(each_course)

    return retCode


def save_course_table_extend_info_into_database(class_info_to_save, user=''):
    output = ""
    count = 0
    for eachCourse in class_info_to_save:
        now = datetime.now()

        if not eachCourse[3]:
            language = '中文'
        else:
            language = eachCourse[3]
        search_result = CourseInfo.objects.all().filter(course_id=eachCourse[0])
        if search_result:
            CourseInfo.objects.filter(id=search_result[0].id).update(major=eachCourse[2],
                                                                     language=language,
                                                                     course_relate=eachCourse[4],
                                                                     update_time=now)
            module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} major {} language {} course_relate {}'.format(eachCourse[0], eachCourse[2], language, eachCourse[4]))
        else:
            search_result = CourseInfo.objects.all().filter(course_name=eachCourse[1])
            if search_result:
                print "1 {}".format(eachCourse)
            else:
                print "2 {}".format(eachCourse)
    return output


@csrf_exempt
def class_get_teacher_name(request):
    teacher_str = request.POST['teacher_str']
    search_result = TeacherInfo.objects.all().filter(teacher_name=teacher_str, lock_state=0)
    status = 'Success'
    if search_result:
        teacher_name = teacher_str
        teacher_id = search_result[0].teacher_id
    else:
        search_result = TeacherInfo.objects.filter(teacher_id=teacher_str,lock_state=0)
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
        if search_result[0].major:
            major = search_result[0].major.strip('学')
        else:
            major = ''
        raw_data.extend([search_result[0].course_name,
                         major,
                         search_result[0].student_type,
                         tmp_class_grade,
                         tmp_class_name,
                         search_result[0].semester,
                         str(int(search_result[0].course_hour)),
                         str(search_result[0].course_degree),
                         search_result[0].course_type,
                         search_result[0].language,
                         search_result[0].allow_teachers,
                         search_result[0].times_every_week,
                         search_result[0].course_relate,
                         search_result[0].excellent_course])
    if raw_data:
        status = 'Success'
    else:
        status = 'Fail'

    result = json.dumps({'raw_data': raw_data, 'status':status})
    return HttpResponse(result)


@login_required()
def arrange_class(request):
    step_info = []
    init_info = {}
    step_position = ['active', 'disabled', 'disabled', 'disabled', 'disabled']
    current_year_init = datetime.now().year
    select_year = ['{}-{}'.format(current_year_init-1, current_year_init),
                   '{}-{}'.format(current_year_init, current_year_init+1),
                   '{}-{}'.format(current_year_init+1, current_year_init+2)]
    init_info['select_year'] = select_year
    search_result = CurrentStepInfo.objects.all()
    if len(search_result) == 1:
        if search_result[0].arrange_class_status == 'start':
            step_info.append(search_result[0].s1_year_info)
            step_position[1] = 'active'
            if search_result[0].s2_undergraduate:

                step_info.append(int(search_result[0].s2_undergraduate) % 3)
            if search_result[0].s2_postgraduate_1:
                step_info.append(int(search_result[0].s2_postgraduate_1) % 3)
            if search_result[0].s2_postgraduate_2:
                step_info.append(int(search_result[0].s2_postgraduate_2) % 3)
            if search_result[0].s2_doctor:
                step_info.append(int(search_result[0].s2_doctor) % 3)
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
                step_info.append(int(search_result[0].s2_teacher_confirm_u) % 3)
            if search_result[0].s2_teacher_confirm_p1:
                step_info.append(int(search_result[0].s2_teacher_confirm_p1) % 3)
            if search_result[0].s2_teacher_confirm_p2:
                step_info.append(int(search_result[0].s2_teacher_confirm_p2) % 3)
            if search_result[0].s2_teacher_confirm_d:
                step_info.append(int(search_result[0].s2_teacher_confirm_d) % 3)

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
            if search_result[0].s5_status_flag == 'lock start' or search_result[0].s5_status_flag == 'unlock':
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

    times = [[current_year_init-1,current_year_init,current_year_init+1],[i for i in range(1, 13)], [i for i in range(1, 32)], [i for i in range(24)], [i for i in range(1, 60)]]
    init_info['times'] = times
    return render(request, 'arrange_class.html', {'UserName': request.user.last_name+request.user.first_name+request.user.username, 'step_info': step_info,
                                                  'step_position': step_position, 'times':init_info['times'], 'select_year':init_info['select_year']})


@csrf_exempt
def arrange_step_1(request):
    year = request.POST['year']
    search_result = CurrentStepInfo.objects.all()
    CourseAdjustInfo.objects.all().delete()
    user = request.user.last_name+request.user.first_name+request.user.username
    module_log_update.data_operate_log(user, '[CourseAdjustInfo] Delete ALL')
    if search_result:
        CurrentStepInfo.objects.filter(id=search_result[0].id).update(s1_year_info=year)
        result = 'success'
    else:
        CurrentStepInfo.objects.create(arrange_class_status='start', s1_year_info=year, s2_undergraduate='0', s2_postgraduate_1='0',
                                       s2_postgraduate_2='0', s2_doctor='0', s2_teacher_confirm_u='0',s2_teacher_confirm_p1='0',s2_teacher_confirm_p2='0',s2_teacher_confirm_d='0')
        result = 'success'

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
            if int(tmp[0].s2_undergraduate) % 3 == 2 and int(tmp[0].s2_postgraduate_1) % 3 == 2 and \
               int(tmp[0].s2_postgraduate_2) % 3 == 2 and int(tmp[0].s2_doctor) % 3 == 2:
                CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_start_request='1')
                result = 'start request'
        if len(tmp) == 1 and 's2_r3' in button_id:
            if int(tmp[0].s2_teacher_confirm_u) % 3 == 2 and int(tmp[0].s2_teacher_confirm_p1) % 3 == 2 and \
               int(tmp[0].s2_teacher_confirm_p2) % 3 == 2 and int(tmp[0].s2_teacher_confirm_d) % 3 == 2:
                CurrentStepInfo.objects.filter(id=search_result[0].id).update(s2_start_request='2')
                result = 'request end'
    result = json.dumps({'result': result})
    return HttpResponse(result)


@csrf_exempt
def arrange_step_3(request):
    status = request.POST['status']
    result = {}
    result['status'] = 'Pass'
    operator = request.user.last_name + request.user.first_name + request.user.username
    search_result = CurrentStepInfo.objects.all()
    if len(search_result) == 1:
        if status == 'start arrange':
            CurrentStepInfo.objects.filter(id=search_result[0].id).update(s3_status_flag=status)
        elif status == 'init info':
            result['info'] = start_arrange()
        elif status == 'arrange main':
            try:
                arrange_main(user=operator)
            except Exception, e:
                module_log_update.log_info('class_manage', '排课异常:{}'.format(e))
                result = 'Fail'
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
    search_result_course = CourseInfo.objects.all().filter(lock_state=0)
    search_result_teacher = TeacherInfo.objects.all().filter(lock_state=0)
    teacher_count = len(search_result_teacher)
    teacher_with_expect = []
    teacher_without_expect = []
    expect_count = 0
    total_count = 0
    lock_teacher_count = len(TeacherInfo.objects.all().filter(lock_state=1))
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
        tmp_hour, tmp_degree = get_course_effective_point(eachCourse)
        total_hours += tmp_hour
        if eachCourse.student_type == STUDENT_TYPE[3]:
            degree_count_d[int(eachCourse.course_degree)-1] += 1
            hours_d.append(tmp_hour)
        elif eachCourse.student_type == STUDENT_TYPE[2]:
            degree_count_p2[int(eachCourse.course_degree)-1] += 1
            hours_p2.append(tmp_hour)
        elif eachCourse.student_type == STUDENT_TYPE[1]:
            degree_count_p1[int(eachCourse.course_degree) - 1] += 1
            hours_p1.append(tmp_hour)
        elif eachCourse.student_type == STUDENT_TYPE[0]:
            degree_count_u[int(eachCourse.course_degree) - 1] += 1
            hours_u.append(tmp_hour)
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
            degree_count, total_courses, [degree_count_u, degree_count_p1, degree_count_p2, degree_count_d], lock_teacher_count]


def arrange_main(user='admin'):
    now = datetime.now().strftime("%Y-%m-%d %H-%M")
    file_obj = open('analysis_result.txt', 'w+')
    module_name = 'class_manage'
    search_result_course = CourseInfo.objects.all().filter(lock_state=0)
    search_result_teacher = TeacherInfo.objects.all().filter(lock_state=0)
    teacher_1 = {}
    teacher_2 = {}
    result_1 = {}
    result_2 = []
    # 权重值
    total_weight = [0, 0]
    for eachTeacher in search_result_teacher:
        birthday_date = eachTeacher.birthday
        tmp_dict = {'id': eachTeacher.teacher_id, 'expect_1': eachTeacher.first_semester_expect,
                    'expect_2': eachTeacher.second_semester_expect, 'total_1': 0, 'total_2': 0,
                    'birthday':birthday_date, 'sex':eachTeacher.sex, 'approaching_retirement':False}
        if eachTeacher.first_semester_expect != 0:
            total_weight[0] += float(eachTeacher.first_semester_expect)
        if eachTeacher.second_semester_expect != 0:
            total_weight[1] += float(eachTeacher.second_semester_expect)
        if eachTeacher.sex == '女' and (eachTeacher.teacher_title == '讲师'):
            if (datetime.now().date() - birthday_date).days >= 53*365:
                tmp_dict['approaching_retirement'] = True
        if eachTeacher.sex == '男':
            if (datetime.now().date() - birthday_date).days >= 58*365:
                tmp_dict['approaching_retirement'] = True

        teacher_1[eachTeacher.teacher_name] = tmp_dict
        teacher_2[eachTeacher.teacher_id] = eachTeacher.teacher_name

    total_hours = [0, 0]
    total_degrees = [0, 0]
    for eachCourse in search_result_course:
        tmp_hour, tmp_degree = get_course_effective_point(eachCourse)
        if eachCourse.semester == '一':
            total_hours[0] += tmp_hour
            total_degrees[0] += tmp_degree
        else:
            total_hours[1] += tmp_hour
            total_degrees[1] += tmp_degree
    hours_ave_1 = total_hours[0]/total_weight[0]
    hours_ave_2 = total_hours[1]/total_weight[1]
    degree_ave_1 = total_degrees[0]/total_weight[0]
    degree_ave_2 = total_degrees[1]/total_weight[1]
    # # 关于一个学分取整
    # hours_ave_1 = (hours_ave_1 / 18 + 1) * 18
    # hours_ave_2 = (hours_ave_2 / 18 + 1) * 18
    print >>file_obj, '<STEP0 Initial teacher state>'
    module_log_update.log_info(module_name, '<STEP0 Initial teacher state> user: {}'.format(user))
    for eachTeacher in search_result_teacher:
        expect_hours_1 = math.ceil(eachTeacher.first_semester_expect * hours_ave_1 / 18) * 18
        expect_hours_2 = math.ceil(eachTeacher.second_semester_expect * hours_ave_2 / 18) * 18
        expect_degree_1 = eachTeacher.first_semester_expect * degree_ave_1
        expect_degree_2 = eachTeacher.second_semester_expect * degree_ave_2
        print >>file_obj, "工号:{} 姓名:{} 第一学期期望学时:{} 第二学期期望学时:{} 第一学期期望难度:{} 第二学期期望难度:{}".format(
            eachTeacher.teacher_id, eachTeacher.teacher_name, expect_hours_1, expect_hours_2, expect_degree_1, expect_degree_2)

        module_log_update.log_info(module_name, "工号:{} 姓名:{} 第一学期期望学时:{} 第二学期期望学时:{} 第一学期期望难度:{} 第二学期期望难度:{}".format(
            eachTeacher.teacher_id, eachTeacher.teacher_name, expect_hours_1, expect_hours_2, expect_degree_1, expect_degree_2))

        tmp_dict = {'course_list': [], 'degree_list': [], 'total_hours_1': 0, 'expect_hours_1': expect_hours_1, 'total_hours_2': 0,
                    'expect_hours_2': expect_hours_2, 'expect_degree_1': expect_degree_1, 'expect_degree_2': expect_degree_2,
                    'total_degree_1': 0, 'total_degree_2': 0}
        result_1[eachTeacher.teacher_id] = tmp_dict

    result_1, result_2 = first_allocation_for_limit_teacher_list(result_1, search_result_course, teacher_1, file_obj)

    # print >>file_obj, '<STEP 1 Limitation for teacher list>'
    # for eachCourse in search_result_course:
    #     teacher_list = eachCourse.suit_teacher.split(',')
    #     if len(teacher_list) == int(eachCourse.allow_teachers):
    #         for eachTeacher in teacher_list:
    #             # print eachTeacher
    #             result_1[teacher_1[eachTeacher]['id']]['course_list'].append(eachCourse.course_id)
    #             result_1[teacher_1[eachTeacher]['id']]['degree_list'].append(eachCourse.course_degree)
    #             if eachCourse.semester == '一':
    #                 tmp_str1 = 'total_hours_1'
    #                 tmp_str2 = 'total_degree_1'
    #             else:
    #                 tmp_str1 = 'total_hours_2'
    #                 tmp_str2 = 'total_degree_2'
    #             result_1[teacher_1[eachTeacher]['id']][tmp_str1] += int(eachCourse.course_hour)/int(eachCourse.allow_teachers)
    #             result_1[teacher_1[eachTeacher]['id']][tmp_str2] += int(eachCourse.course_degree)/float(eachCourse.allow_teachers)
    #     else:
    #         result_2.append(eachCourse)
    show_statistical(result_1, file_obj)
    result_2_firstSemester, result_2_secondSemester = split_semester_from_whole_year(result_2)
    for each_semester in [result_2_firstSemester, result_2_secondSemester]:
        # 难度均衡
        result_1, result_2 = balance_for_high_degree(result_1, each_semester, teacher_1, file_obj)
        show_statistical(result_1, file_obj)
        # 学时均衡
        result_1, result_2 = balance_for_course_hour(result_1, result_2, teacher_1, file_obj)
        show_statistical(result_1, file_obj)

    result_3 = {}
    for tmpKey in result_1.keys():
        for eachCourse in result_1[tmpKey]['course_list']:
            if CourseInfo.objects.get(course_id=eachCourse).semester == '一':
                TeacherInfo.objects.filter(teacher_id=tmpKey).update(first_semester_hours=result_1[tmpKey]['total_hours_1'], first_semester_degree=result_1[tmpKey]['total_degree_1'])
                module_log_update.data_operate_log(user, '[TeacherInfo] teacher_id: {} first_semester_hours: {} first_semester_degree: {}'.format(
                    tmpKey,
                    result_1[tmpKey]['total_hours_1'],
                    result_1[tmpKey]['total_degree_1']
                ))
            else:
                TeacherInfo.objects.filter(teacher_id=tmpKey).update(second_semester_hours=result_1[tmpKey]['total_hours_2'], second_semester_degree=result_1[tmpKey]['total_degree_2'])
                module_log_update.data_operate_log(user, '[TeacherInfo] teacher_id: {} second_semester_hours: {} second_semester_degree: {}'.format(
                    tmpKey,
                    result_1[tmpKey]['total_hours_2'],
                    result_1[tmpKey]['total_degree_2']
                ))
            if eachCourse not in result_3.keys():
                result_3[eachCourse] = [teacher_2[tmpKey]]
            else:
                result_3[eachCourse].append(teacher_2[tmpKey])
    for tmpKey in result_3.keys():
        tmp = ",".join(result_3[tmpKey])
        CourseInfo.objects.filter(course_id=tmpKey).update(teacher_auto_pick=tmp, teacher_final_pick=tmp)
        module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} teacher_auto_pick {} teacher_final_pick {}'.format(tmpKey, tmp, tmp))
        current_course = CourseInfo.objects.filter(course_id=tmpKey)
        if current_course:
            course_relate = current_course[0].course_relate.split(',')
            for eachCourse in course_relate:
                CourseInfo.objects.filter(course_id=eachCourse).update(teacher_auto_pick=tmp, teacher_final_pick=tmp)
                module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} teacher_auto_pick {} teacher_final_pick {}'.format(eachCourse, tmp, tmp))
    file_obj.close()
    # HttpResponse('Pass')


def show_statistical(result_1, file_obj):
    print >>file_obj, '##########################################################'
    print >>file_obj, 'showing available information'
    module_name = 'class_manage'
    module_log_update.log_info(module_name, '##########################################################')
    module_log_update.log_info(module_name, 'showing available information')
    for tmpKey in result_1.keys():
        avail_hours_1 = result_1[tmpKey]['expect_hours_1'] - result_1[tmpKey]['total_hours_1']
        avail_hours_2 = result_1[tmpKey]['expect_hours_2'] - result_1[tmpKey]['total_hours_2']
        avail_degree_1 = result_1[tmpKey]['expect_degree_1'] - result_1[tmpKey]['total_degree_1']
        avail_degree_2 = result_1[tmpKey]['expect_degree_2'] - result_1[tmpKey]['total_degree_2']
        print >>file_obj, 'teacher id: {} available hours {} {} available degree {} {}'.format(tmpKey, avail_hours_1, avail_hours_2,
                                                                                   avail_degree_1, avail_degree_2)
        module_log_update.log_info(module_name, 'teacher id: {} available hours {} {} available degree {} {}'.format(tmpKey, avail_hours_1, avail_hours_2,
                                                                                   avail_degree_1, avail_degree_2))
        # logging.info('teacher id: {} available hours {} {} available degree {} {}'.format(tmpKey, avail_hours_1, avail_hours_2,
        #                                                                            avail_degree_1, avail_degree_2))
    print >>file_obj, '##########################################################'
    module_log_update.log_info(module_name, '##########################################################')


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
            tmp = sorted(eachItem, key=lambda x: len(x.teacher_ordered.split(',')))
            result_list.extend(tmp)
        else:
            result_list.append(eachItem[0])
    # for eachItem in result_list:
    #     print eachItem.course_hour
    #     print len(eachItem.suit_teacher.split(','))
    return result_list


# 先available学时排序 再 available难度排序
def sort_new_2(result_list, result_all_teacher, key_value_1, key_value_2, key_value_3, key_value_4, teacher_info):
    if key_value_2 == 'total_hours_1' and key_value_1 == 'expect_hours_1':
        result_list = sorted(result_list, key=lambda x: (result_all_teacher[x][key_value_1]-result_all_teacher[x][key_value_2]), reverse=True)
    # available 学时考虑另外一个学期。如果目前是第二学期，学时均衡需要考虑到第一学期的负荷
    elif key_value_2 == 'total_hours_2' and key_value_1 == 'expect_hours_2':
        result_list = sorted(result_list,
                         key=lambda x: (
                         result_all_teacher[x]['expect_hours_1'] + result_all_teacher[x]['expect_hours_2'] -
                         result_all_teacher[x]['total_hours_1'] - result_all_teacher[x]['total_hours_2']),
                         reverse=True)
    else:
        pass
        # logging.error('unknown string at sort_new_2 {} {}'.format(key_value_1, key_value_2))
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
            tmp = sort_new_3(tmp, result_all_teacher, key_value_3, key_value_4,teacher_info)
            result_list.extend(tmp)
        else:
            result_list.append(eachItem[0])
    # for eachItem in result_list:
    #     print 'teacher id {}'.format(eachItem)
    #     print 'left course hour {}'.format((result_all_teacher[eachItem][key_value_1]-result_all_teacher[eachItem][key_value_2]))
    #     print 'left degree {}'.format((result_all_teacher[eachItem][key_value_3]-result_all_teacher[eachItem][key_value_4]))
    return result_list

# 再剩余难度和剩余学时都一样的情况下，优先选择临近退休的老师。女讲师55岁，其余60岁
def sort_new_3(result_list, result_all_teacher, key_value_1, key_value_2, teacher_info):
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
            for teacher_id in eachItem:
                teacher_by_id = TeacherInfo.objects.get(teacher_id=teacher_id)
                if teacher_info[teacher_by_id.teacher_name]['approaching_retirement'] == True:
                    # logging.info('teacher id: {} is chose with high priority than others {}, because of approaching retirement'.format(teacher_id, eachItem))
                    eachItem.remove(teacher_id)
                    eachItem.insert(0,teacher_id)

            result_list.extend(eachItem)
        else:
            result_list.append(eachItem[0])

    return result_list


def high_level_factor_involve(result_list, result_all_teacher, key_value_1, key_value_2, key_value_3, key_value_4,
                              teacher_info, current_course_hour, current_course_degree, current_course_id):
    teacher_candidate_list1 = []
    teacher_left1 = []
    logging.info('teacher list: {}'.format(result_list))
    for each_teacher in result_list:
        if result_all_teacher[each_teacher][key_value_1] - result_all_teacher[each_teacher][
            key_value_2] - current_course_hour > 0:
            if result_all_teacher[each_teacher][key_value_3] - result_all_teacher[each_teacher][
                key_value_4] - current_course_degree > 0:
                logging.info(
                    'teacher id: {} is chose with high priority than others {}, because of approaching retirement'.format(
                        each_teacher, teacher_candidate_list1))
                teacher_candidate_list1.append(each_teacher)
            else:
                teacher_left1.append(each_teacher)
        else:
            teacher_left1.append(each_teacher)
    logging.info('teacher candidate list1: {}; left1: {}'.format(teacher_candidate_list1, teacher_left1))
    # 轮替
    teacher_candidate_list2 = []
    teacher_left2 = []
    search_course_history = CourseHistoryInfo.objects.filter(course_id=current_course_id)
    if search_course_history:
        teacher_final_pick_list = []
        for each_year in search_course_history:
            year = each_year.year
            teacher_final_pick = each_year.teacher_final_pick.split(',') if each_year.teacher_final_pick else []
            teacher_id_list = []
            for each_teacher in teacher_final_pick:
                search_result = TeacherInfo.objects.filter(teacher_name=each_teacher)
                if search_result:
                    teacher_id_list.append(search_result[0].teacher_id)
            teacher_final_pick_list.append([year.split('-')[0], teacher_id_list])
        tmp = sorted(teacher_final_pick_list, key=lambda x: x[0], reverse=True)
        for each_teacher in teacher_candidate_list1:
            teachered = False
            for each_year in tmp:
                if each_teacher not in each_year[1]:
                    teachered = False
                else:
                    teachered = True
            if not teachered:
                logging.info('{} is priority because of not teacher this course {} before'.format(each_teacher,
                                                                                                  current_course_id))
                teacher_candidate_list2.append(each_teacher)
            else:
                teacher_left2.append(each_teacher)

    logging.info('teacher candidate list2: {}; left2: {}'.format(teacher_candidate_list2, teacher_left2))
    # 临近退休
    teacher_candidate_list3 = []
    teacher_left3 = []
    for each_teacher in teacher_candidate_list1:
        teacher_by_id = TeacherInfo.objects.get(teacher_id=each_teacher)
        if teacher_info[teacher_by_id.teacher_name]['approaching_retirement'] == True:
            logging.info(
                'teacher id: {} is chose with high priority than others {}, because of approaching retirement'.format(
                    each_teacher, teacher_candidate_list1))
            teacher_candidate_list3.append(each_teacher)
        else:
            teacher_left3.append(each_teacher)
    logging.info('teacher candidate list3: {}; left3: {}'.format(teacher_candidate_list3, teacher_left3))
    if len(teacher_candidate_list3) != 0:
        # teacher_candidate_list1(teacher_candidate_list2+teacher_left2) + teacher_left1
        result_list = teacher_candidate_list3 + teacher_left3 + teacher_left1
    elif len(teacher_candidate_list2) != 0:
        # teacher_candidate_list1(teacher_candidate_list2+teacher_left2) + teacher_left1
        result_list = teacher_candidate_list2 + teacher_left2 + teacher_left1
    else:
        result_list = result_list

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


def split_semester_from_whole_year(result_courses):
    first_semester = []
    second_semester = []
    for each_course in result_courses:
        if each_course.semester == '一':
            first_semester.append(each_course)
        elif each_course.semester == '二':
            second_semester.append(each_course)
        else:
            pass
            # logging.error('this course is abnormal with unknown semester: {}'.format(each_course))
    return first_semester, second_semester


def balance_for_high_degree(result_all_teachers, result_left_courses, teacher_info, file_obj):
    print >>file_obj, '<STEP 2 high degree course balance>'
    module_name = 'class_manage'
    module_log_update.log_info(module_name, '<STEP 2 high degree course balance>')
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
            print >>file_obj, eachCourse.course_id
            module_log_update.log_info(module_name, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            module_log_update.log_info(module_name, eachCourse.course_id)
            teacher_list = eachCourse.teacher_ordered.split(',')
            all_teachers = int(eachCourse.allow_teachers)
            # 平行课程的教师数要乘以平行班数
            if eachCourse.course_parallel > 1:
                all_teachers = int(eachCourse.allow_teachers) * int(eachCourse.course_parallel)
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
                print eachTeacher
                teacher_id_list.append(teacher_info[eachTeacher]['id'])

            high_degree_count = 0
            for eachTeacher in teacher_id_list:
                print >>file_obj, 'teacher id {}'.format(eachTeacher)
                print >>file_obj, '<current> course list {}'.format(result_all_teachers[eachTeacher]['course_list'])
                print >>file_obj, '<current> degree list {}'.format(result_all_teachers[eachTeacher]['degree_list'])
                print >>file_obj, '<current> hour left {}'.format(
                    (result_all_teachers[eachTeacher][tmp_str2] - result_all_teachers[eachTeacher][tmp_str1]))
                print >>file_obj, '<current> degree left {}'.format(
                    (result_all_teachers[eachTeacher][tmp_str4] - result_all_teachers[eachTeacher][tmp_str3]))
                module_log_update.log_info(module_name, 'teacher id {}'.format(eachTeacher))
                module_log_update.log_info(module_name, '<current> course list {}'.format(result_all_teachers[eachTeacher]['course_list']))
                module_log_update.log_info(module_name, '<current> degree list {}'.format(result_all_teachers[eachTeacher]['degree_list']))
                module_log_update.log_info(module_name, '<current> hour left {}'.format(
                    (result_all_teachers[eachTeacher][tmp_str2] - result_all_teachers[eachTeacher][tmp_str1])))
                module_log_update.log_info(module_name, '<current> degree left {}'.format(
                    (result_all_teachers[eachTeacher][tmp_str4] - result_all_teachers[eachTeacher][tmp_str3])))

            while all_teachers > 0:
                current_list = find_high_degree_course_count(teacher_id_list, high_degree_count, result_all_teachers)
                if len(current_list) > 1:
                    current_list = sort_new_2(current_list, result_all_teachers, tmp_str2, tmp_str1, tmp_str4, tmp_str3, teacher_info)
                if len(current_list) == 0:
                    high_degree_count += 1
                    continue
                print >>file_obj, '<current> teacher list {}. high degree count {}'.format(current_list, high_degree_count)
                module_log_update.log_info(module_name, '<current> teacher list {}. high degree count {}'.format(current_list, high_degree_count))

                if result_all_teachers[current_list[0]][tmp_str1] + eachCourse.course_hour <= result_all_teachers[current_list[0]][tmp_str2]:
                    # high level factor design
                    current_list = high_level_factor_involve(current_list, result_all_teachers, tmp_str2, tmp_str1,
                                                             tmp_str4, tmp_str3, teacher_info, eachCourse.course_hour,
                                                             eachCourse.course_degree, eachCourse.course_id)
                    print >>file_obj, '<choose> teacher id {}'.format(current_list[0])
                    print >>file_obj, '<before choose> total hours {}'.format(result_all_teachers[current_list[0]][tmp_str1])
                    print >>file_obj, '<before choose> degree list {}'.format(result_all_teachers[current_list[0]]['degree_list'])
                    module_log_update.log_info(module_name, '<choose> teacher id {}'.format(current_list[0]))
                    module_log_update.log_info(module_name, '<before choose> total hours {}'.format(result_all_teachers[current_list[0]][tmp_str1]))
                    module_log_update.log_info(module_name, '<before choose> degree list {}'.format(result_all_teachers[current_list[0]]['degree_list']))

                    result_all_teachers[current_list[0]]['course_list'].append(eachCourse.course_id)
                    result_all_teachers[current_list[0]]['degree_list'].append(eachCourse.course_degree)
                    # 平行课程和非平行课程的计算方法不同
                    # allow_teachers = float(eachCourse.allow_teachers)/float(eachCourse.course_parallel) if eachCourse.course_parallel else float(eachCourse.allow_teachers)
                    # 新代码里eachCourse.allow_teachers就是单课需要的老师数
                    allow_teachers = float(eachCourse.allow_teachers)
                    result_all_teachers[current_list[0]][tmp_str1] += eachCourse.course_hour / allow_teachers
                    result_all_teachers[current_list[0]][tmp_str3] += eachCourse.course_degree / allow_teachers
                    all_teachers -= 1
                    teacher_id_list.remove(current_list[0])
                    high_degree_count = 0
                    print >>file_obj, '<after choose> total hours {}'.format(result_all_teachers[current_list[0]][tmp_str1])
                    print >>file_obj, '<after choose> degree list {}'.format(result_all_teachers[current_list[0]]['degree_list'])
                    module_log_update.log_info(module_name, '<after choose> total hours {}'.format(result_all_teachers[current_list[0]][tmp_str1]))
                    module_log_update.log_info(module_name, '<after choose> degree list {}'.format(result_all_teachers[current_list[0]]['degree_list']))

                else:
                    high_degree_count += 1
                    if len(current_list) == len(teacher_id_list):
                        print >> file_obj, '<BAD 1> all teacher hours are exceed expect'
                        module_log_update.log_info(module_name, '<BAD 1> all teacher hours are exceed expect')
                        for i in range(all_teachers):
                            print >>file_obj, '<BAD 1>teacher id {}'.format(current_list[i])
                            print >>file_obj, '<BAD 1>total hours {}'.format(result_all_teachers[current_list[i]][tmp_str1])
                            print >>file_obj, '<BAD 1>degree list {}'.format(result_all_teachers[current_list[i]]['degree_list'])
                            module_log_update.log_info(module_name, '<BAD 1>teacher id {}'.format(current_list[i]))
                            module_log_update.log_info(module_name, '<BAD 1>total hours {}'.format(result_all_teachers[current_list[i]][tmp_str1]))
                            module_log_update.log_info(module_name, '<BAD 1>degree list {}'.format(result_all_teachers[current_list[i]]['degree_list']))

                            result_all_teachers[current_list[i]]['course_list'].append(eachCourse.course_id)
                            result_all_teachers[current_list[i]]['degree_list'].append(eachCourse.course_degree)
                            # 平行课程和非平行课程的计算方法不同
                            #allow_teachers = float(eachCourse.allow_teachers) / float(
                            #    eachCourse.course_parallel) if eachCourse.course_parallel else float(
                            #    eachCourse.allow_teachers)
                            # 新代码里eachCourse.allow_teachers就是单课需要的老师数
                            allow_teachers = float(eachCourse.allow_teachers)
                            result_all_teachers[current_list[i]][tmp_str1] += eachCourse.course_hour / allow_teachers
                            result_all_teachers[current_list[i]][tmp_str3] += eachCourse.course_degree / allow_teachers
                            all_teachers -= 1
                            print >>file_obj, '<BAD 1>new total hours {}'.format(result_all_teachers[current_list[i]][tmp_str1])
                            print >>file_obj, '<BAD 1>new degree list {}'.format(result_all_teachers[current_list[i]]['degree_list'])
                            module_log_update.log_info(module_name, '<BAD 1>new total hours {}'.format(result_all_teachers[current_list[i]][tmp_str1]))
                            module_log_update.log_info(module_name, '<BAD 1>new degree list {}'.format(result_all_teachers[current_list[i]]['degree_list']))

            print >>file_obj, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
            module_log_update.log_info(module_name, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    for eachItem in tmp_teacher_in_high_degree_course:
        print >>file_obj, '{} {}'.format(eachItem, result_all_teachers[eachItem]['degree_list'])
        module_log_update.log_info(module_name, '{} {}'.format(eachItem, result_all_teachers[eachItem]['degree_list']))
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
    module_name = 'class_manage'
    module_log_update.log_info(module_name, '<STEP 3 course hour balance>')
    for eachCourse in result_left_courses:
        print >>file_obj, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print >>file_obj, eachCourse.course_id
        module_log_update.log_info(module_name, 'course id:{}'.format(eachCourse.course_id))
        logging.info(eachCourse.course_id)
        all_teachers = int(eachCourse.allow_teachers)
        # 平行课程的教师数要乘以平行班数
        if eachCourse.course_parallel > 1:
            all_teachers = int(eachCourse.allow_teachers) * int(eachCourse.course_parallel)
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
        tmp = eachCourse.teacher_ordered.split(',')
        teacher_list = []
        for eachTeacher in tmp:
            teacher_list.append(teacher_info[eachTeacher]['id'])
        for eachTeacher in teacher_list:
            print >>file_obj, 'teacher id {}'.format(eachTeacher)
            print >>file_obj, '<current> course list {}'.format(result_all_teachers[eachTeacher]['course_list'])
            print >>file_obj, '<current> degree list {}'.format(result_all_teachers[eachTeacher]['degree_list'])
            print >>file_obj, '<current> hour left {}'.format(
                (result_all_teachers[eachTeacher][tmp_str2] - result_all_teachers[eachTeacher][tmp_str1]))
            print >>file_obj, '<current> total hour 1:{} 2:{}'.format(result_all_teachers[eachTeacher]['total_hours_1'],result_all_teachers[eachTeacher]['total_hours_2'])
            print >>file_obj, '<current> degree left {}'.format(
                (result_all_teachers[eachTeacher][tmp_str4] - result_all_teachers[eachTeacher][tmp_str3]))
            module_log_update.log_info(module_name, 'teacher id {}'.format(eachTeacher))
            module_log_update.log_info(module_name, '<current> course list {}'.format(result_all_teachers[eachTeacher]['course_list']))
            module_log_update.log_info(module_name, '<current> degree list {}'.format(result_all_teachers[eachTeacher]['degree_list']))
            module_log_update.log_info(module_name, '<current> hour left {}'.format(
                (result_all_teachers[eachTeacher][tmp_str2] - result_all_teachers[eachTeacher][tmp_str1])))
            module_log_update.log_info(module_name, '<current> total hour 1:{} 2:{}'.format(result_all_teachers[eachTeacher]['total_hours_1'],result_all_teachers[eachTeacher]['total_hours_2']))
            module_log_update.log_info(module_name, '<current> degree left {}'.format(
                (result_all_teachers[eachTeacher][tmp_str4] - result_all_teachers[eachTeacher][tmp_str3])))

        teacher_list = sort_new_2(teacher_list, result_all_teachers, tmp_str2, tmp_str1, tmp_str4, tmp_str3,teacher_info)
        print >> file_obj, '<current> after sort_new_2 course list {}'.format(teacher_list)
        module_log_update.log_info(module_name, '<current> after sort_new_2 course list {}'.format(teacher_list))
        # high level factor design
        teacher_list = high_level_factor_involve(teacher_list, result_all_teachers, tmp_str2, tmp_str1,
                                                 tmp_str4, tmp_str3, teacher_info, eachCourse.course_hour,
                                                 eachCourse.course_degree, eachCourse.course_id)
        print >> file_obj, '<current> after high_level_factor_involve course list {}'.format(teacher_list)
        module_log_update.log_info(module_name, '<current> after high_level_factor_involve course list {}'.format(teacher_list))

        for i in range(all_teachers):
            print >>file_obj, '<choose> teacher id {}'.format(teacher_list[i])
            print >>file_obj, '<before> total hours {}'.format(result_all_teachers[teacher_list[i]][tmp_str1])
            print >>file_obj, '<before> degree list {}'.format(result_all_teachers[teacher_list[i]]['degree_list'])
            module_log_update.log_info(module_name, '<choose> teacher id {}'.format(teacher_list[i]))
            module_log_update.log_info(module_name, '<before> total hours {}'.format(result_all_teachers[teacher_list[i]][tmp_str1]))
            module_log_update.log_info(module_name, '<before> degree list {}'.format(result_all_teachers[teacher_list[i]]['degree_list']))

            result_all_teachers[teacher_list[i]]['course_list'].append(eachCourse.course_id)
            result_all_teachers[teacher_list[i]]['degree_list'].append(eachCourse.course_degree)
            # 新代码里的allow_teachers就是eachCourse.allow_teachers
            # allow_teachers = float(eachCourse.allow_teachers) / float(
            #     eachCourse.course_parallel) if eachCourse.course_parallel else float(
            #     eachCourse.allow_teachers)
            allow_teachers = eachCourse.allow_teachers
            result_all_teachers[teacher_list[i]][tmp_str1] += eachCourse.course_hour / allow_teachers
            result_all_teachers[teacher_list[i]][tmp_str3] += eachCourse.course_degree / allow_teachers
            all_teachers -= 1
            print >>file_obj, '<after choose> new total hours {}'.format(result_all_teachers[teacher_list[i]][tmp_str1])
            print >>file_obj, '<after choose> new degree list {}'.format(result_all_teachers[teacher_list[i]]['degree_list'])
            module_log_update.log_info(module_name, '<after choose> new total hours {}'.format(result_all_teachers[teacher_list[i]][tmp_str1]))
            module_log_update.log_info(module_name, '<after choose> new degree list {}'.format(result_all_teachers[teacher_list[i]]['degree_list']))

    return result_all_teachers, result_left_courses


def first_allocation_for_limit_teacher_list(result_all_teachers, result_left_courses, teacher_info, file_obj):
    print >> file_obj, '<STEP 1 Limitation for teacher list>'
    module_name = 'class_manage'
    module_log_update.log_info(module_name, '<STEP 1 Limitation for teacher list>')
    result_2 = []
    for eachCourse in result_left_courses:
        module_log_update.log_info(module_name, '课程：{} 计算实际需要的老师数'.format(eachCourse.course_id))
        # 本科 - 硕士 打通课程的时候，排课时以本科的课程为主进行排课
        if eachCourse.course_relate and eachCourse.student_type != '本科':
            continue
        if int(eachCourse.course_parallel) == 1:
            # 非平行课实际需要的人数
            teacher_limit_final = int(eachCourse.allow_teachers)
            module_log_update.log_info(module_name, '非平行课程，实际需要老师数：{}'.format(teacher_limit_final))
        else:
            # 平行课实际需要的人数
            teacher_limit_final = eachCourse.allow_teachers * int(eachCourse.course_parallel)
            module_log_update.log_info(module_name, '平行课程，实际需要老师数：{}'.format(teacher_limit_final))
        teacher_list = eachCourse.teacher_ordered.split(',')
        if len(teacher_list) == teacher_limit_final:
            module_log_update.log_info(module_name, '申报人数正好和实际需要老师数相等')
            for eachTeacher in teacher_list:
                print eachTeacher
                result_all_teachers[teacher_info[eachTeacher]['id']]['course_list'].append(eachCourse.course_id)
                result_all_teachers[teacher_info[eachTeacher]['id']]['degree_list'].append(eachCourse.course_degree)
                if eachCourse.semester == '一':
                    tmp_str1 = 'total_hours_1'
                    tmp_str2 = 'total_degree_1'
                else:
                    tmp_str1 = 'total_hours_2'
                    tmp_str2 = 'total_degree_2'
                result_all_teachers[teacher_info[eachTeacher]['id']][tmp_str1] += int(eachCourse.course_hour) / int(
                    eachCourse.allow_teachers)
                result_all_teachers[teacher_info[eachTeacher]['id']][tmp_str2] += int(eachCourse.course_degree) / float(
                    eachCourse.allow_teachers)
        else:
            module_log_update.log_info(module_name, '申报人数和实际需要老师数不相等')
            if int(eachCourse.course_parallel) == 1:
                module_log_update.log_info(module_name, '非平行课程直接进入下一轮排课循环')
                result_2.append(eachCourse)
            else:
                # 平行班级情况下，如果申报认识不满足最高要求，但是大于最低要求，会先行安排
                module_log_update.log_info(module_name, '课程：{} 平行班级情况下，如果申报认识不满足最高要求，但是大于最低要求，会先行安排'.format(eachCourse))
                teacher_limit_basic = eachCourse.allow_teachers
                if len(teacher_list) > teacher_limit_final:
                    module_log_update.log_info(module_name, '平行课程申报人数大于实际需要老师数的进入下一轮排课循环')
                    result_2.append(eachCourse)
                elif teacher_limit_basic <= len(teacher_list) < teacher_limit_final:
                    # 平行班级情况下，如果申报人数不满足最高要求，但是大于最低要求，会先行安排
                    #module_log_update.log_info(module_name, '课程：{} 平行班级情况下，如果申报人数不满足最高要求，但是大于最低要求，会先行安排'.format(eachCourse.course_id))
                #teacher_limit_final = eachCourse.allow_teachers * int(eachCourse.course_parallel)
                #if len(teacher_list) == teacher_limit_final:
                #    module_log_update.log_info(module_name, '平行班申报人数正好满足最高要求')
                #    result_2.append(eachCourse)
                    module_log_update.log_info(module_name, '平行班申报人数满足最低要求，但是不足最高要求')
                    for eachTeacher in teacher_list:
                        print eachTeacher
                        result_all_teachers[teacher_info[eachTeacher]['id']]['course_list'].append(
                            eachCourse.course_id)
                        result_all_teachers[teacher_info[eachTeacher]['id']]['degree_list'].append(
                            eachCourse.course_degree)
                        if eachCourse.semester == '一':
                            tmp_str1 = 'total_hours_1'
                            tmp_str2 = 'total_degree_1'
                        else:
                            tmp_str1 = 'total_hours_2'
                            tmp_str2 = 'total_degree_2'
                        result_all_teachers[teacher_info[eachTeacher]['id']][tmp_str1] += int(
                            eachCourse.course_hour) / int(
                            eachCourse.allow_teachers)
                        result_all_teachers[teacher_info[eachTeacher]['id']][tmp_str2] += int(
                            eachCourse.course_degree) / float(
                            eachCourse.allow_teachers)
                    left_course_time = teacher_limit_final - len(teacher_list)
                    for eachTeacher in teacher_list:
                        print eachTeacher
                        result_all_teachers[teacher_info[eachTeacher]['id']]['course_list'].append(
                            eachCourse.course_id)
                        result_all_teachers[teacher_info[eachTeacher]['id']]['degree_list'].append(
                            eachCourse.course_degree)
                        if eachCourse.semester == '一':
                            tmp_str1 = 'total_hours_1'
                            tmp_str2 = 'total_degree_1'
                        else:
                            tmp_str1 = 'total_hours_2'
                            tmp_str2 = 'total_degree_2'
                        result_all_teachers[teacher_info[eachTeacher]['id']][tmp_str1] += int(
                            eachCourse.course_hour) / int(
                            eachCourse.allow_teachers)
                        result_all_teachers[teacher_info[eachTeacher]['id']][tmp_str2] += int(
                            eachCourse.course_degree) / float(
                            eachCourse.allow_teachers)
                        left_course_time -= 1
                        if left_course_time == 0:
                            break

    return result_all_teachers, result_2



@csrf_exempt
def arrange_export_report(request):
    now = datetime.now().strftime("%Y-%m-%d %H-%M")
    ws = xlwt.Workbook(encoding='utf-8')
    w = ws.add_sheet(u"排课结果")
    course_table = CourseInfo.objects.filter()
    search_result = []
    for eachItem in course_table:
        search_result.append([eachItem.course_id,
                              eachItem.course_name,
                              eachItem.major,
                              eachItem.student_type,
                              eachItem.year,
                              eachItem.class_name,
                              eachItem.semester,
                              eachItem.course_hour,
                              eachItem.course_degree,
                              eachItem.course_type,
                              eachItem.allow_teachers,
                              eachItem.times_every_week,
                              eachItem.teacher_final_pick,
                              eachItem.course_relate,
                              eachItem.language,
                              eachItem.excellent_course,
                              eachItem.lock_state,
                              eachItem.course_parallel])

    table_head = ['代码', '名称', '学科', '学位', '学年', '班级', '学期', '学时', '难度', '必/选', '教师数', '周上课次数', '上课老师', '打通课程代码','上课语言','是否精品课程','是否激活','平行班级数']
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
    print >>file_obj, '教师总数: {}\r\n'.format(total_info[0])
    print >> file_obj, '有{}位教师有期望学时, 总计{}学时\r\n'.format(total_info[1], total_info[2])
    print >> file_obj, '其余{}位教师, 预计平均学时为{}学时\r\n'.format(total_info[3], total_info[4])
    print >> file_obj, '预计各难度平均分配教师:\r\n'
    for index, eachLine in enumerate(total_info[5], 1):
        print >> file_obj, '  {} {}\r\n'.format((11-index), eachLine)
    print >> file_obj, '课程总数{}\r\n'.format(total_info[6])
    for index, eachLine in enumerate(STUDENT_TYPE):
        print >> file_obj, '{}\r\n'.format(eachLine)
        for j, eachItem in enumerate(total_info[7][index], 1):
            if j == 1:
                print >> file_obj,'  各课程各难度数:\r\n'
            elif j == 11:
                print >> file_obj, '  各课程各学时数:\r\n'
            else:
                pass

            if 1 <= j < 11:
                print >> file_obj, '  {} {}\r\n'.format(11 - j, eachItem)
            if j >= 11:
                print >> file_obj, '  {} {}\r\n'.format(COURSE_HOUR[j % 11], eachItem)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={}_{}.txt'.format('analysis_report_2', now)
    file_obj.close()
    file_obj = open('statistical_result.txt', 'rb+').read()
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
        course_parallel = int(search_result[0].course_parallel)
        teacher_pick = search_result[0].teacher_final_pick
        teacher_ordered = search_result[0].teacher_ordered
        teacher_list = teacher_pick.split(',') if teacher_pick else []
        teacher_ordered_list = teacher_ordered.split(',') if teacher_ordered else []
        tmp1 = []
        for eachTeacher in teacher_list:
            teacher_table = TeacherInfo.objects.filter(teacher_name=eachTeacher)
            if teacher_table:
                teacher_id = teacher_table[0].teacher_id
                tmp1.append([teacher_id, eachTeacher])
            else:
                status = '原授课教师信息有误 {}'.format(eachTeacher)
        tmp2 = []
        for eachTeacher in teacher_ordered_list:
            teacher_table = TeacherInfo.objects.filter(teacher_name=eachTeacher)
            if teacher_table:
                teacher_id = teacher_table[0].teacher_id
                tmp2.append([teacher_id, eachTeacher])
        search_result = CourseAdjustInfo.objects.filter(course_id=course_id)
        if search_result:
            notes = search_result[0].notes
        else:
            notes = ''
        result = [course_name, student_type, semester, class_name, course_degree, course_hour, times_every_week,
                  allow_teachers, tmp2, tmp1,notes, course_parallel]
    else:
        status = '找不到该课程号码对应的课程'
        result = []

    result = json.dumps({'course': result, 'status': status})
    return HttpResponse(result)

@csrf_exempt
def arrange_submit_adjust_request(request):
    course_id = request.POST['course_id']
    to_change_teacher = request.POST['to_change_teacher']
    notes = request.POST['notes']
    user = request.user.last_name + request.user.first_name + request.user.username
    try:
        search_result = CourseInfo.objects.filter(course_id=course_id)
        course_name = search_result[0].course_name
        teacher_before = search_result[0].teacher_final_pick
        origin_teacher_list = search_result[0].teacher_final_pick.split(',') if teacher_before else []
        teacher_ordered = search_result[0].teacher_ordered if search_result[0].teacher_ordered else []
        to_change_teacher_list = to_change_teacher.split(',')
        tmp_list = []
        for eachTeacher in to_change_teacher_list:
            if eachTeacher in teacher_ordered:
                tmp_list.append('{}(已申报)'.format(eachTeacher))
            else:
                tmp_list.append('{}(未申报)'.format(eachTeacher))
        to_change_teacher = ','.join(tmp_list)
        tmp_list = []
        for eachTeacher in origin_teacher_list:
            if eachTeacher not in teacher_ordered:
                tmp_list.append('{}(未申报)'.format(eachTeacher))
            else:
                tmp_list.append(eachTeacher)
        origin_teacher_list = ','.join(tmp_list)
        if not CourseAdjustInfo.objects.filter(course_id=course_id):
            CourseAdjustInfo.objects.create(course_id=course_id,
                                            course_name=course_name,
                                            teacher_before=origin_teacher_list,
                                            teacher_after=to_change_teacher,
                                            status='等待审批',
                                            notes=notes)
            module_log_update.data_operate_log(user, '[CourseAdjustInfo] course_id: {} course_name: {} teacher_before: {} teacher_after: {} status: {} notes'.format(
                course_id,
                course_name,
                origin_teacher_list,
                to_change_teacher,
                '等待审批',
                notes
            ))
        else:
            CourseAdjustInfo.objects.filter(course_id=course_id).update(teacher_before=origin_teacher_list,
                                                                        teacher_after=to_change_teacher,
                                                                        status='等待审批',
                                                                        notes=notes)
            module_log_update.data_operate_log(user, '[CourseAdjustInfo] course_id: {} teacher_before: {} teacher_after: {} status: {} notes'.format(
                course_id,
                origin_teacher_list,
                to_change_teacher,
                '等待审批',
                notes
            ))
        status = 'success'
    except Exception, e:
        print e
        status = '修改失败 错误信息{}'.format(e)

    result = json.dumps({'status': status})
    return HttpResponse(result)

@csrf_exempt
def arrange_change_by_course_id(request):
    course_id = request.POST['course_id']
    to_change_teacher = request.POST['to_change_teacher']
    user = request.user.last_name + request.user.first_name + request.user.username
    try:
        search_result = CourseInfo.objects.filter(course_id=course_id)
        final_teacher_list = search_result[0].teacher_final_pick.split(',')
        course_hour = search_result[0].course_hour / (len(final_teacher_list) if final_teacher_list else 1)
        course_degree = search_result[0].course_degree / (len(final_teacher_list) if final_teacher_list else 1)
        semester = search_result[0].semester
        for eachTeacher in final_teacher_list:
            teacher_result = TeacherInfo.objects.filter(teacher_name=eachTeacher)
            if semester == '一':
                value1 = float(teacher_result[0].first_semester_hours if teacher_result[0].first_semester_hours else 0) - float(course_hour)
                value2 = float(teacher_result[0].first_semester_degree if teacher_result[0].first_semester_degree else 0) - float(course_degree)
                TeacherInfo.objects.filter(teacher_name=eachTeacher).update(first_semester_hours=value1,
                                                                            first_semester_degree=value2)
                module_log_update.data_operate_log(user, '[TeacherInfo] teacher_name: {} first_semester_hours: {} first_semester_degree: {}'.format(
                    eachTeacher,
                    value1,
                    value2
                ))
            else:
                value1 = float(teacher_result[0].second_semester_hours if teacher_result[0].second_semester_hours else 0) - float(course_hour)
                value2 = float(teacher_result[0].second_semester_degree if teacher_result[0].second_semester_degree else 0) - float(course_degree)
                TeacherInfo.objects.filter(teacher_name=eachTeacher).update(second_semester_hours=value1,
                                                                            second_semester_degree=value2)
                module_log_update.data_operate_log(user, '[TeacherInfo] teacher_name: {} second_semester_hours: {} second_semester_degree: {}'.format(
                    eachTeacher,
                    value1,
                    value2
                ))
        to_change_teacher_list = to_change_teacher.split(',')
        for eachTeacher in to_change_teacher_list:
            teacher_result = TeacherInfo.objects.filter(teacher_name=eachTeacher)
            if semester == '一':

                value1 = float(teacher_result[0].first_semester_hours if teacher_result[0].first_semester_hours else 0) + float(course_hour)
                value2 = float(teacher_result[0].first_semester_degree if teacher_result[0].first_semester_degree else 0) + float(course_degree)
                TeacherInfo.objects.filter(teacher_name=eachTeacher).update(first_semester_hours=value1,
                                                                            first_semester_degree=value2)
                module_log_update.data_operate_log(user, '[TeacherInfo] teacher_name: {} first_semester_hours: {} first_semester_degree: {}'.format(
                    eachTeacher,
                    value1,
                    value2
                ))
            else:
                value1 = float(teacher_result[0].second_semester_hours if teacher_result[0].second_semester_hours else 0) + float(course_hour)
                value2 = float(teacher_result[0].second_semester_degree if teacher_result[0].second_semester_degree else 0) + float(course_degree)
                TeacherInfo.objects.filter(teacher_name=eachTeacher).update(second_semester_hours=value1,
                                                                            second_semester_degree=value2)
                module_log_update.data_operate_log(user, '[TeacherInfo] teacher_name: {} second_semester_hours: {} second_semester_degree: {}'.format(
                    eachTeacher,
                    value1,
                    value2
                ))

        CourseInfo.objects.filter(course_id=course_id).update(teacher_final_pick=to_change_teacher)
        module_log_update.data_operate_log(user, '[CourseInfo]update: course_id {} teacher_final_pick {}'.format(course_id, to_change_teacher))
        search_result_course = CourseInfo.objects.filter(course_id=course_id)
        if search_result_course[0].course_relate:
            if search_result_course[0].student_type == '本科':
                course_list = search_result_course[0].course_relate.split(',')
                for eachCourse in course_list:
                    CourseInfo.objects.filter(course_id=eachCourse).update(teacher_final_pick=to_change_teacher)
                    module_log_update.data_operate_log(user,
                                                       '[CourseInfo]update: course_id {} teacher_final_pick {}'.format(eachCourse, to_change_teacher))
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


def update_final_result(current_year):
    status = 'Success'
    result_course_info = CourseInfo.objects.all()
    CourseHistoryInfo.objects.filter(year=current_year).delete()
    for each_course in result_course_info:
        course_adjust_hist = CourseAdjustInfo.objects.filter(course_id=each_course.course_id, status='已批准')
        tmp_notes_list = [each_course.notes if each_course.notes else '']
        if course_adjust_hist:
            tmp_notes_list.append(course_adjust_hist[0].notes)

        if CourseHistoryInfo.objects.filter(course_id=each_course.course_id, year=current_year):
            CourseHistoryInfo.objects.update(course_id=each_course.course_id,
                                             course_name=each_course.course_name,
                                             student_type=each_course.student_type,
                                             year=current_year,
                                             class_name=each_course.class_name,
                                             semester=each_course.semester,
                                             course_hour=each_course.course_hour,
                                             course_degree=each_course.course_degree,
                                             course_type=each_course.course_type,
                                             allow_teachers=each_course.allow_teachers,
                                             times_every_week=each_course.times_every_week,
                                             suit_teacher=each_course.suit_teacher,
                                             teacher_ordered=each_course.teacher_ordered,
                                             teacher_auto_pick=each_course.teacher_auto_pick,
                                             teacher_final_pick=each_course.teacher_final_pick,
                                             excellent_course=each_course.excellent_course,
                                             major=each_course.major,
                                             language=each_course.language,
                                             course_relate=each_course.course_relate,
                                             lock_state=each_course.lock_state,
                                             notes='/'.join(tmp_notes_list),
                                             course_parallel=each_course.course_parallel)
        else:
            CourseHistoryInfo.objects.create(course_id=each_course.course_id,
                                             course_name=each_course.course_name,
                                             student_type=each_course.student_type,
                                             year=current_year,
                                             class_name=each_course.class_name,
                                             semester=each_course.semester,
                                             course_hour=each_course.course_hour,
                                             course_degree=each_course.course_degree,
                                             course_type=each_course.course_type,
                                             allow_teachers=each_course.allow_teachers,
                                             times_every_week=each_course.times_every_week,
                                             suit_teacher=each_course.suit_teacher,
                                             teacher_ordered=each_course.teacher_ordered,
                                             teacher_auto_pick=each_course.teacher_auto_pick,
                                             teacher_final_pick=each_course.teacher_final_pick,
                                             excellent_course=each_course.excellent_course,
                                             major=each_course.major,
                                             language=each_course.language,
                                             course_relate=each_course.course_relate,
                                             lock_state=each_course.lock_state,
                                             notes='/'.join(tmp_notes_list),
                                             course_parallel=each_course.course_parallel)
    return status


@csrf_exempt
def arrange_step_5(request):
    operation_status = request.POST['status']
    search_result = CurrentStepInfo.objects.all()
    status = '切换至最后一步失败'
    user_type = request.user.nickname
    user = request.user.last_name + request.user.first_name + request.user.username
    if operation_status:
        if len(search_result) == 1:
            search_adjust_result = CourseAdjustInfo.objects.filter(status='等待审批')
            if not search_adjust_result:
                status = 'Success'
                if operation_status == 'lock done':
                    if user_type == 'leader':
                        module_log_update.data_operate_log(user, '[lock done]')
                        update_final_result(search_result[0].s1_year_info)
                    else:
                        status = '您没有权限锁定排课'
                elif operation_status == 'unlock':
                    if user_type == 'leader':
                        CurrentStepInfo.objects.filter(id=search_result[0].id).update(s5_status_flag=operation_status)
                    else:
                        status = '您没有权限解锁'
                else:
                    pass
                if status == 'Success':
                    CurrentStepInfo.objects.filter(id=search_result[0].id).update(s5_status_flag=operation_status)

            else:
                status = '还有未处理的微调申请'
        else:
            status = '没有找到正在进行的排课'
    result = json.dumps({'status': status})
    return HttpResponse(result)

@csrf_exempt
def history_search_by_year(request):
    year = request.POST['year']
    search_result = CourseHistoryInfo.objects.filter(year=year)
    class_table = []
    init_data = []

    init_data.append(year)
    for eachItem in search_result:
        if eachItem.course_relate and eachItem.student_type != '本科':
            continue
        class_name_list = eachItem.class_name.split(' ')
        if eachItem.course_relate and eachItem.student_type == '本科':
            course_relate_list = eachItem.course_relate.split(',')
            for eachCourseId in course_relate_list:
                if CourseHistoryInfo.objects.filter(year=year,course_id=eachCourseId):
                    class_name_list.extend(CourseHistoryInfo.objects.filter(year=year,course_id=eachCourseId)[0].class_name.split(' '))
        # todo when class name confirm, may change
        # class_name_str = ' / '.join((' '.join(class_name_list)).split(' '))
        class_name_str = get_class_name(class_name_list)
        if eachItem.course_relate:
            course_relate = eachItem.course_relate.strip(',')
            course_id_str = '{} / {}'.format(eachItem.course_id, course_relate)
            student_type_relate = CourseHistoryInfo.objects.filter(course_id=course_relate)[0].student_type
            student_type_str = '{} / {}'.format(eachItem.student_type, student_type_relate)
        else:
            course_id_str = eachItem.course_id
            student_type_str = eachItem.student_type

        class_table.append([course_id_str,
                            eachItem.course_name,
                            eachItem.major,
                            student_type_str,
                            class_name_str,
                            eachItem.semester,
                            eachItem.course_hour,
                            eachItem.course_degree,
                            eachItem.course_type,
                            eachItem.language,
                            eachItem.allow_teachers,
                            eachItem.times_every_week,
                            eachItem.course_parallel,
                            get_excellent_course(eachItem.excellent_course),
                            get_teacher_final_pick(eachItem.teacher_final_pick, eachItem.teacher_ordered),
                            eachItem.teacher_ordered,
                            '非激活' if eachItem.lock_state else '',
                            eachItem.notes if eachItem.notes else ''])
    result = json.dumps({'class_table': class_table, 'init_data': init_data})
    return HttpResponse(result)


@csrf_exempt
def history_export_report(request):
    now = datetime.now().strftime("%Y-%m-%d %H-%M")
    ws = xlwt.Workbook(encoding='utf-8')
    w = ws.add_sheet(u"课程信息")
    year = request.GET.get('current_year')
    course_table = CourseHistoryInfo.objects.filter(year=year)
    search_result = []
    for eachItem in course_table:
        for eachClass in eachItem.class_name.split(' '):
            tmp_student = eachClass.split('-')[0]
            tmp_class_grade, tmp_class_name = eachClass.split('-')[-1].split('_')
            if eachItem.course_relate:
                course_relate = eachItem.course_relate.strip(',')
            else:
                course_relate = ''
            # search_result.append([eachItem.course_id,
            #                       eachItem.course_name,
            #                       eachItem.major,
            #                       tmp_student,
            #                       tmp_class_grade,
            #                       tmp_class_name,
            #                       eachItem.semester,
            #                       eachItem.course_hour,
            #                       eachItem.course_degree,
            #                       eachItem.course_type,
            #                       eachItem.language,
            #                       eachItem.allow_teachers,
            #                       eachItem.times_every_week,
            #                       eachItem.teacher_final_pick,
            #                       course_relate,
            #                       eachItem.excellent_course,
            #                       eachItem.course_parallel
            #                       ])
            search_result.append([eachItem.year,
                                  eachItem.semester,
                                  eachItem.student_type,
                                  tmp_class_grade,
                                  tmp_class_name,
                                  eachItem.major,
                                  eachItem.course_id,
                                  eachItem.course_name,
                                  eachItem.course_hour / 18,
                                  eachItem.course_hour,
                                  eachItem.course_degree,
                                  eachItem.course_type,
                                  eachItem.language,
                                  eachItem.allow_teachers,
                                  eachItem.times_every_week,
                                  eachItem.teacher_ordered,
                                  course_relate,
                                  get_excellent_course(eachItem.excellent_course),
                                  eachItem.course_parallel,
                                  '非激活' if eachItem.lock_state else '',
                                  get_teacher_final_pick(eachItem.teacher_final_pick, eachItem.teacher_ordered),
                                  eachItem.teacher_ordered,
                                  eachItem.notes if eachItem.notes else ''
                                  ])

    table_head = ['学年','学期','学位','年级','班级','专业','课程代码','课程名称','学分','学时','难度','必修/选修','授课语言','教师数','每周上课次数',
                              '可选教师','打通课程代码','是否精品课程','平行班级','状态','授课教师','申报教师','备注']
    for col, eachTitle in enumerate(table_head):
        w.write(0, col, eachTitle)
    for row, eachRow in enumerate(search_result):
        for col, eachCol in enumerate(eachRow):
            w.write(row+1, col, eachCol)
    exist_file = os.path.exists("历史信息汇总.xls")
    if exist_file:
        os.remove(r"历史信息汇总.xls")
    filename = '历史信息汇总'
    ws.save("{}.xls".format(filename))
    sio = BytesIO()
    ws.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/ms-excel')

    filename = urlquote(filename)
    response['Content-Disposition'] = 'attachment; filename={}_{}.xls'.format(filename, now)
    response.write(sio.getvalue())
    return response


@csrf_exempt
def history_export_teacher(request):
    now = datetime.now().strftime("%Y-%m-%d %H-%M")
    ws = xlwt.Workbook(encoding='utf-8')
    w = ws.add_sheet(u"历史结果")
    year = request.GET.get('current_year')
    if not year:
        course_table = CourseInfo.objects.filter(lock_state=0)
    else:
        course_table = CourseHistoryInfo.objects.filter(year=year, lock_state=0)
    teacher_info = {}
    for eachItem in course_table:
        if eachItem.teacher_final_pick:
            teacher_list = eachItem.teacher_final_pick.split(',')
        else:
            continue
        if eachItem.course_relate and eachItem.student_type != '本科':
            continue
        for eachTeacher in teacher_list:
            if eachTeacher not in teacher_info.keys():
                teacher_info[eachTeacher] = {'id':'',
                                             'degree_first_semester': 0,
                                             'degree_second_semester': 0,
                                             'hour_first_semester':0,
                                             'hour_second_semester':0,
                                             'course_list':[]}
            if eachItem.semester == '一':
                teacher_info[eachTeacher]['degree_first_semester'] += int(eachItem.course_degree)
                teacher_info[eachTeacher]['hour_first_semester'] += int(eachItem.course_hour)
            else:
                teacher_info[eachTeacher]['degree_second_semester'] += int(eachItem.course_degree)
                teacher_info[eachTeacher]['hour_second_semester'] += int(eachItem.course_hour)
            teacher_info[eachTeacher]['course_list'].append(eachItem.course_id)
    teacher_info_list = []
    for tmpKey in teacher_info.keys():
        teacher_info_list.append([tmpKey, teacher_info[tmpKey]['degree_first_semester'], teacher_info[tmpKey]['hour_first_semester'],
                                 teacher_info[tmpKey]['degree_second_semester'],teacher_info[tmpKey]['hour_second_semester'],len(teacher_info[tmpKey]['course_list'])])
    table_head = ['教师', '第一学期难度', '第一学期学时', '第二学期难度', '第二学期学时', '总共授课']

    for col, eachTitle in enumerate(table_head):
        w.write(0, col, eachTitle)
    for row, eachRow in enumerate(teacher_info_list):
        for col, eachCol in enumerate(eachRow):
            w.write(row+1, col, eachCol)
    exist_file = os.path.exists("教师授课情况汇总.xls")
    if exist_file:
        os.remove(r"教师授课情况汇总.xls")
    filename = '教师授课情况汇总'
    ws.save("{}.xls".format(filename))
    sio = BytesIO()
    ws.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/ms-excel')

    filename = urlquote(filename)
    response['Content-Disposition'] = 'attachment; filename={}_{}.xls'.format(filename, now)
    response.write(sio.getvalue())
    return response


@login_required()
def class_history_history_main(request):
    table_head = ['代码', '名称', '专业', '学位', '班级', '学期', '学时', '难度', '必/选', '语言', '教师数', '周上课次数', '平行班级', '是否精品课程', '上课教师','申报教师','状态','备注']
    exist_years = []
    init_data = []
    search_result = CourseHistoryInfo.objects.values('year')
    for eachResult in search_result:
        if eachResult['year'] not in exist_years:
            exist_years.append(eachResult['year'])
    exist_years = sorted(exist_years)

    search_result = CurrentStepInfo.objects.all()
    if search_result:
        year = search_result[0].s1_year_info
        init_data.append(year)
    else:
        return render(request, 'class_management_history.html',
                  {'UserName': request.user.last_name + request.user.first_name + request.user.username,
                   'class_table': [],
                   'table_head': table_head,
                   'exist_years': exist_years,
                   'init_data': init_data,
                   })
    search_result = CourseHistoryInfo.objects.filter(year=year)
    class_table = []
    for eachItem in search_result:
        if eachItem.course_relate and eachItem.student_type != '本科':
            continue
        class_name_list = eachItem.class_name.split(' ')
        if eachItem.course_relate and eachItem.student_type == '本科':
            course_relate_list = eachItem.course_relate.split(',')
            for eachCourseId in course_relate_list:
                if CourseHistoryInfo.objects.filter(year=year,course_id=eachCourseId):
                    class_name_list.extend(CourseHistoryInfo.objects.filter(year=year,course_id=eachCourseId)[0].class_name.split(' '))
        # todo when class name confirm, may change
        # class_name_str = ' / '.join((' '.join(class_name_list)).split(' '))
        class_name_str = get_class_name(class_name_list)
        if eachItem.course_relate:
            course_relate = eachItem.course_relate.strip(',')
            course_id_str = '{} / {}'.format(eachItem.course_id, course_relate)
            student_type_relate = CourseHistoryInfo.objects.filter(year=year,course_id=course_relate)[0].student_type
            student_type_str = '{} / {}'.format(eachItem.student_type, student_type_relate)
        else:
            course_id_str = eachItem.course_id
            student_type_str = eachItem.student_type

        class_table.append([course_id_str,
                              eachItem.course_name,
                              eachItem.major,
                              student_type_str,
                              class_name_str,
                              eachItem.semester,
                              eachItem.course_hour,
                              eachItem.course_degree,
                              eachItem.course_type,
                              eachItem.language,
                              eachItem.allow_teachers,
                              eachItem.times_every_week,
                              eachItem.course_parallel,
                              get_excellent_course(eachItem.excellent_course),
                              get_teacher_final_pick(eachItem.teacher_final_pick, eachItem.teacher_ordered),
                              eachItem.teacher_ordered,
                              '非激活' if eachItem.lock_state else '',
                              eachItem.notes if eachItem.notes else ''])
    return render(request, 'class_management_history.html',
                  {'UserName': request.user.last_name + request.user.first_name + request.user.username,
                   'class_table': class_table,
                   'table_head': table_head,
                   'exist_years': exist_years,
                   'init_data': init_data,
                   })
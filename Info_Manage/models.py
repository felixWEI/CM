# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class TeacherInfo(models.Model):
    teacher_id = models.IntegerField(db_column='teacher_id')
    teacher_name = models.CharField(db_column='teacher_name', max_length=45, blank=True, null=True)
    first_semester = models.FloatField(db_column='first_semester', blank=True, null=True)
    second_semester = models.FloatField(db_column='second_semester', blank=True, null=True)
    claiming_course = models.CharField(db_column='claiming_course', max_length=1000, blank=True, null=True)
    update_time = models.DateTimeField(db_column='update_time', blank=True, null=True)

    def as_dict(self):
        return {
            "teacher_id": self.teacher_id,
            "teacher_name": self.teacher_name,
            "first_semester": self.first_semester,
            "second_semester": self.second_semester,
            "claiming_course": self.claiming_course,
            "update_time": self.update_time,
        }

    class Meta:
        managed = False
        db_table = 'teacher_info'


class CourseInfo(models.Model):
    course_id = models.CharField(db_column='course_id', max_length=45, blank=True, null=True)
    course_name = models.CharField(db_column='course_name', max_length=45, blank=True, null=True)
    student_type = models.CharField(db_column='student_type', max_length=45, blank=True, null=True)
    year = models.CharField(db_column='year', max_length=45, blank=True, null=True)
    class_name = models.CharField(db_column='class_name', max_length=45, blank=True, null=True)
    semester = models.CharField(db_column='semester', max_length=45, blank=True, null=True)
    course_hour = models.FloatField(db_column='course_hour', blank=True, null=True)
    course_degree = models.FloatField(db_column='course_degree', blank=True, null=True)
    course_type = models.CharField(db_column='course_type', max_length=45, blank=True, null=True)
    allow_teachers = models.IntegerField(db_column='allow_teachers')
    times_every_week = models.IntegerField(db_column='times_every_week')
    suit_teacher = models.CharField(db_column='suit_teacher', max_length=200, blank=True, null=True)
    update_time = models.DateTimeField(db_column='update_time', blank=True, null=True)

    def as_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "course_hour": self.course_hour,
            "course_degree": self.course_degree,
            "student_type": self.student_type,
            "class_name": self.class_name,
            "times_every_week": self.times_every_week,
            "suit_teacher": self.suit_teacher,
            "course_type": self.course_type,
            "allow_teachers": self.allow_teachers,
            "semester": self.semester,
            "year": self.year,
            "update_time": self.update_time,
        }

    class Meta:
        managed = False
        db_table = 'course_info'

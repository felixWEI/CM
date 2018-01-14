# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class TeacherInfo(models.Model):
    teacher_id = models.IntegerField(db_column='teacher_id')
    teacher_name = models.CharField(db_column='teacher_name', max_length=45, blank=True, null=True)
    first_semester = models.FloatField(db_column='first_semester', blank=True, null=True)
    second_semester = models.FloatField(db_column='second_semester', blank=True, null=True)
    claiming_course = models.FloatField(db_column='claiming_course', max_length=1000, blank=True, null=True)
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

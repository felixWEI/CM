# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import CourseInfo, TeacherInfo, CurrentStepInfo
from django.contrib import admin

# Register your models here.
admin.site.register((CourseInfo, TeacherInfo, CurrentStepInfo))

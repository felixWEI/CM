"""ClassManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from Home.views import home_page, logout_view
from Info_Manage.views import teacher_manage, teacher_personal, class_manage, teacher_change_expect, teacher_request_course,\
                        arrange_class, teacher_save_and_config, teacher_table_upload, class_save_one_row, class_delete_one_row, \
                        class_get_suit_teacher, class_table_upload, arrange_step_1, arrange_step_2, arrange_step_3, \
                        arrange_export_report, class_get_teacher_name, class_filter_by_submit, arrange_search_by_course_id, \
                        arrange_change_by_course_id, arrange_change_button_status, arrange_step_5, \
    class_search_from_course_id, teacher_submit_apply_status, arrange_export_analysis_1, arrange_export_analysis_2
from Info_Search.views import info_search_main

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', login, {'template_name': 'registration\login.html'}),
    url(r'^accounts/logout/$', logout_view),
    url(r'^users/', include('users.urls')),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^$', home_page, name='home'),
    url(r'^teacher_manage/', teacher_manage),
    url(r'^teacher_personal/', teacher_personal),
    url(r'^teacher_save_and_config/', teacher_save_and_config),
    url(r'^teacher_request_course/', teacher_request_course),
    url(r'^teacher_table_upload/', teacher_table_upload),
    url(r'^teacher_change_expect/', teacher_change_expect),
    url(r'^teacher_submit_apply_status/', teacher_submit_apply_status),
    url(r'^class_manage/', class_manage),
    url(r'^class_save_one_row/', class_save_one_row),
    url(r'^class_delete_one_row/', class_delete_one_row),
    url(r'^class_get_suit_teacher/', class_get_suit_teacher),
    url(r'^class_table_upload/', class_table_upload),
    url(r'^class_get_teacher_name', class_get_teacher_name),
    url(r'^class_filter_by_submit/', class_filter_by_submit),
    url(r'^class_search_from_course_id/', class_search_from_course_id),
    url(r'^arrange_class/', arrange_class),
    url(r'^arrange_step_1/', arrange_step_1),
    url(r'^arrange_step_2/', arrange_step_2),
    url(r'^arrange_step_3/', arrange_step_3),
    url(r'^arrange_export_report/', arrange_export_report),
    url(r'^arrange_export_analysis_1/', arrange_export_analysis_1),
    url(r'^arrange_export_analysis_2/', arrange_export_analysis_2),
    url(r'^arrange_search_by_course_id/', arrange_search_by_course_id),
    url(r'^arrange_change_by_course_id/', arrange_change_by_course_id),
    url(r'^arrange_change_button_status/', arrange_change_button_status),
    url(r'^arrange_step_5/', arrange_step_5),
    url(r'^info_search/', info_search_main),
]

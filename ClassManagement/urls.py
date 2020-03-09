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
from Info_Manage import views as Info_Manage_views
from Info_Search.views import info_search_main

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', login, {'template_name': 'registration\login.html'}),
    url(r'^accounts/logout/$', logout_view),
    url(r'^users/', include('users.urls')),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^$', home_page, name='home'),
    url(r'^teacher_leader/', Info_Manage_views.teacher_leader),
    url(r'^teacher_reject_teacher_adjust', Info_Manage_views.teacher_reject_teacher_adjust),
    url(r'^teacher_approve_teacher_adjust', Info_Manage_views.teacher_approve_teacher_adjust),
    url(r'^teacher_manage/', Info_Manage_views.teacher_manage),
    url(r'^teacher_manage_adjust/', Info_Manage_views.teacher_manage_adjust),
    url(r'^teacher_personal/', Info_Manage_views.teacher_personal),
    url(r'^teacher_personal_lock/', Info_Manage_views.teacher_personal_lock),
    url(r'^teacher_save_and_config/', Info_Manage_views.teacher_save_and_config),
    url(r'^teacher_request_course/', Info_Manage_views.teacher_request_course),
    url(r'^teacher_table_upload/', Info_Manage_views.teacher_table_upload),
    url(r'^teacher_help_declare_upload/', Info_Manage_views.teacher_help_declare_upload, name="teacher_help_declare_upload"),
    url(r'^teacher_change_expect/', Info_Manage_views.teacher_change_expect),
    url(r'^teacher_submit_apply_status/', Info_Manage_views.teacher_submit_apply_status),
    url(r'^check_teacher_apply_status/', Info_Manage_views.check_teacher_apply_status),
    url(r'^class_manage/', Info_Manage_views.class_manage),
    url(r'^class_save_one_row/', Info_Manage_views.class_save_one_row),
    url(r'^class_delete_one_row/', Info_Manage_views.class_delete_one_row),
    url(r'^class_get_suit_teacher/', Info_Manage_views.class_get_suit_teacher),
    url(r'^class_table_upload/', Info_Manage_views.class_table_upload),
    url(r'^class_get_teacher_name', Info_Manage_views.class_get_teacher_name),
    url(r'^class_filter_by_submit/', Info_Manage_views.class_filter_by_submit),
    url(r'^class_search_from_course_id/', Info_Manage_views.class_search_from_course_id),
    url(r'^arrange_class/', Info_Manage_views.arrange_class),
    url(r'^arrange_step_1/', Info_Manage_views.arrange_step_1),
    url(r'^arrange_step_2/', Info_Manage_views.arrange_step_2),
    url(r'^arrange_step_3/', Info_Manage_views.arrange_step_3),
    url(r'^arrange_export_report/', Info_Manage_views.arrange_export_report),
    url(r'^arrange_export_analysis_1/', Info_Manage_views.arrange_export_analysis_1),
    url(r'^arrange_export_analysis_2/', Info_Manage_views.arrange_export_analysis_2),
    url(r'^arrange_search_by_course_id/', Info_Manage_views.arrange_search_by_course_id),
    url(r'^arrange_change_by_course_id/', Info_Manage_views.arrange_change_by_course_id),
    url(r'^arrange_submit_adjust_request/', Info_Manage_views.arrange_submit_adjust_request),
    url(r'^arrange_change_button_status/', Info_Manage_views.arrange_change_button_status),
    url(r'^arrange_step_5/', Info_Manage_views.arrange_step_5),
    url(r'^class_history/', Info_Manage_views.class_history_history_main),
    url(r'^history_search_by_year/', Info_Manage_views.history_search_by_year),
    url(r'^history_export_report/', Info_Manage_views.history_export_report),
    url(r'^history_export_teacher/', Info_Manage_views.history_export_teacher),
    url(r'^info_search/', info_search_main),
]

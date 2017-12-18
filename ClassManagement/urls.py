from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import login

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ClassManagement.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'Home.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, {'template_name': 'login.html'})
)

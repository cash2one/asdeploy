#coding:utf-8

import os.path

from django.conf.urls import patterns
from django.views.generic.simple import direct_to_template
from deployment.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

static_files = os.path.join(
    os.path.dirname(__file__), '../deployment/static_files'
)

urlpatterns = patterns('',
    #静态文件路径
    (r'^static_files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static_files}),
    
    #页面路径
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^register/success/$', direct_to_template,
         {'template': 'registration/register_success.html'}),
    
    (r'^$', main_page),
    (r'user/(\w+)/$', user_page),
)

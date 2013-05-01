import os.path
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from ctf import views
site_media = os.path.join(os.path.dirname(__file__), 'site_media')

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #(r'^user/(\w+)/$', user_page),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', views.logout_page, name='logout'),
    url(r'^register/$', views.register_page, name='register'),
    url(r'^register/success/$', views.register_success,name='sucess'),
    url(r'^flag_submit/$', views.flag_submit,name='flag_submit'),
    #{ 'template': 'registration/register_success.html' }),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    #{ 'document_root': site_media }),
   # url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
   # url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
   # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)


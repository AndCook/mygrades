from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('gradebook.views',
                       url(r'^overview/$', 'overview'),
                       url(r'^current_courses/$', 'current_courses'),
                       url(r'^course_detail/(?P<course_id>\w+)/$', 'course_detail'),
)
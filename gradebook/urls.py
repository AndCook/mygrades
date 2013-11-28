from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('gradebook.views',
                       url(r'^overview/', 'overview'),
                       #url(r'^semester_detail/', 'semester_detail'),
                       #url(r'^course_detail/', 'course_detail'),
)
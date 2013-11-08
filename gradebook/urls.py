from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('gradebook.views',
                       url(r'^report_card/', 'report_card'),
                       url(r'^semester_overview/', 'semester_overview'),
                       url(r'^course_detail/', 'course_detail'),
)
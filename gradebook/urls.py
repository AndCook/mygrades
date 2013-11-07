from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('gradebook.views',
                       url(r'^report-card/', 'report_card', name='report-card'),
                       url(r'^semester-overview/', 'semester_overview', name='semester-overview'),
                       url(r'^course-detail/', 'course_detail', name='course-detail'),
)
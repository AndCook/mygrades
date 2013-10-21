from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'mygrades.views.home', name='home'),

    url(r'^home/', 'mygrades.views.home', name='home'),
    url(r'^report-card/', 'mygrades.views.report_card', name='report-card'),
    url(r'^semester-overview/', 'mygrades.views.semester_overview', name='semester-overview'),
    url(r'^course-detail/', 'mygrades.views.course_detail', name='course-detail'),

    url(r'^admin/', include(admin.site.urls)),
)

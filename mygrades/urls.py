from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('mygrades.views',
                       url(r'^$', 'home'),
                       url(r'^about/$', 'about'),

                       url(r'^accounts/', include('accounts.urls')),

                       url(r'^gradebook/', include('gradebook.urls')),

                       url(r'^admin/', include(admin.site.urls)),
)
from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('account.views',
                       url(r'^login/$', 'my_login'),
                       url(r'^signup/$', 'my_signup'),
                       url(r'^change_password/$', 'my_change_password'),
                       url(r'^settings/$', 'my_settings'),
                       url(r'^logout/$', 'my_logout'),
)
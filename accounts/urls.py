from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('accounts.views',
                       url(r'^login/$', 'my_login'),
                       url(r'^signup', 'signup')
)
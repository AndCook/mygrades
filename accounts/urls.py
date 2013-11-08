from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('accounts.views',
                       url(r'^login_page/$', 'login_page'),
                       url(r'^signup_page/$', 'signup_page'),
                       url(r'^login/$', 'my_login'),
                       url(r'^signup', 'my_signup'),
                       url(r'^logout/$', 'my_logout'),
)
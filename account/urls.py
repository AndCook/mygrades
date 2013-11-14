from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('account.views',
                       url(r'^login/$', 'my_login'),
                       url(r'^signup/$', 'my_signup'),
                       url(r'^change_password/$', 'my_change_password'),
                       url(r'^settings/$', 'my_settings'),
                       url(r'^validate_email/(?P<code>\w+)/$', 'my_validate_email'),
                       url(r'^forgot_password/$', 'my_forgot_password_email'),
                       url(r'^forgot_password/(?P<code>\w+)/$', 'my_forgot_password_passwords'),
                       url(r'^logout/$', 'my_logout'),
)
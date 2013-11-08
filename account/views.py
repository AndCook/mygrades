from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change

from account.forms import UserCreateForm, ChangeSettingsForm, UpdatePasswordForm


def my_signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            user_info = form.cleaned_data
            user = User.objects.create_user(username=user_info['username'],
                                            password=user_info['password1'],
                                            email=user_info['email'])
            user.is_active = True
            user.save()

            login(request, user)

            return HttpResponseRedirect('/gradebook/overview/')
        return render_to_response('signup_page.html', {'signup_form': form}, RequestContext(request))
    return Http404


def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/gradebook/overview/')
        else:
            return HttpResponseRedirect('/account/login_page/')

    return Http404


def my_change_password(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST)

        if form.is_valid():
            password_change(request)
            return HttpResponseRedirect('/account/settings/')
        else:
            return HttpResponseRedirect('/account/change_password/')

    return Http404


def login_page(request):
    return render_to_response('login_page.html', RequestContext(request))


def signup_page(request):
    return render_to_response('signup_page.html', RequestContext(request))

@login_required
def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def settings(request):
    return render_to_response('settings.html', {'change_settings_form': ChangeSettingsForm}, RequestContext(request))

@login_required
def change_password(request):
    return render_to_response('change_password.html',
                              {'change_password_form': UpdatePasswordForm},
                              RequestContext(request))

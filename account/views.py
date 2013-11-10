from django.contrib.auth import authenticate, login, logout
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from account.forms import MyLoginForm, MyUserCreationForm, MyChangeSettingsForm, MyPasswordChangeForm


def my_login(request):
    if request.method == 'POST':
        form = MyLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email_field')
            password = form.cleaned_data.get('password_field')

            user = authenticate(username=email, password=password)
            login(request, user)
            return HttpResponseRedirect('/gradebook/overview/')
    else:
        form = MyLoginForm()
    return render_to_response('login_page.html',
                              {'login_form': form},
                              RequestContext(request))


def my_signup(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user_info = form.cleaned_data
            email = user_info['email']
            password = user_info['password1']
            user = User.objects.create_user(username=email,
                                            password=password,
                                            email=email)
            user.first_name = user_info['first_name']
            user.last_name = user_info['last_name']
            user.is_active = True
            user.save()

            login(request, authenticate(username=email, password=password))

            return HttpResponseRedirect('/gradebook/overview/')
    else:
        form = MyUserCreationForm()
    return render_to_response('signup_page.html',
                              {'signup_form': form},
                              RequestContext(request))


@login_required
def my_change_password(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.POST, {'user': request.user})

        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password1'])
            request.user.save()
            return HttpResponseRedirect('/account/settings/')
    else:
        form = MyPasswordChangeForm({'user': request.user})
    return render_to_response('change_password_page.html',
                              {'password_change_form': form},
                              RequestContext(request))


@login_required
def settings_page(request):
    return render_to_response('settings_page.html',
                              {'change_settings_form': MyChangeSettingsForm()},
                              RequestContext(request))


def my_settings(request):
    return HttpResponseRedirect('/account/settings_page/')


def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

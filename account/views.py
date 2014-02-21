from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.util import ErrorList
from django.core.mail import EmailMessage
from account.forms import MyLoginForm, MyUserCreationForm,\
    MyChangeSettingsForm, MyPasswordChangeForm, MyPasswordResetFormEmail, MyPasswordResetFormPasswords
from mygrades.settings import EMAIL_HOST_USER, BASE_PATH
from random import choice
from string import ascii_letters, digits
from account.models import UserProfile
import json


def my_login(request):
    # if the user is already logged in, send them to the current_courses page
    if request.user.is_authenticated():
        return HttpResponseRedirect('/gradebook/current_courses/')

    if request.is_ajax():
        get_action = request.GET['get_action']
        if get_action == 'check_valid_login':
            email = request.GET['email']
            password = request.GET['password']
            valid = authenticate(username=email, password=password) is not None
            return HttpResponse(json.dumps({'is_valid': valid}), mimetype='application/json')

    if request.method == 'POST':
        form = MyLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(username=email, password=password)
            login(request, user)
            return HttpResponseRedirect('/gradebook/current_courses/')
    else:
        form = MyLoginForm()
    return HttpResponseRedirect('/')


def my_signup(request):
    # if the user is already logged in, send them to the current_courses page
    if request.user.is_authenticated():
        return HttpResponseRedirect('/gradebook/current_courses/')

    if request.is_ajax():
        get_action = request.GET['get_action']
        if get_action == 'is_email_unique':
            email = request.GET['email_in_question']
            unique = User.objects.filter(username=email).count() == 0
            return HttpResponse(json.dumps({'is_unique': unique}), mimetype='application/json')

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            #password2 = form.cleaned_data.get('password2')
            #if password1 != password2:
            #    form.errors.setdefault('password1', ErrorList()).append(form.error_messages['password_mismatch'])
            #else:
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username=email,
                                            password=password1,
                                            email=email)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.is_active = False  # user is inactive until email is validated
            user.save()
            prof = UserProfile(user=user)
            prof.save()

            send_validation_email(user)

            login(request, authenticate(username=email, password=password1))

            return HttpResponseRedirect('/account/settings/')
    else:
        form = MyUserCreationForm()
    return HttpResponseRedirect('/')


@login_required
def my_settings(request):
    if request.is_ajax():
        get_action = request.GET['get_action']
        if get_action == 'is_email_unique':
            email = request.GET['email_in_question']
            unique = (User.objects.filter(username=email).count() == 0 or request.user.username == email)
            return HttpResponse(json.dumps({'is_unique': unique}), mimetype='application/json')

    if request.method == 'POST':
        form = MyChangeSettingsForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            if first_name != 'First Name' and first_name.strip() != '':
                request.user.first_name = first_name.strip()

            last_name = form.cleaned_data.get('last_name')
            if last_name != 'Last Name' and last_name.strip() != '':
                request.user.last_name = last_name.strip()

            email = form.cleaned_data.get('email')
            if email != 'Email' and email.strip() != '':
                request.user.username = email.strip()
                request.user.email = email.strip()
                request.user.is_active = False
                send_validation_email(request.user)

            request.user.save()

            return HttpResponseRedirect('/account/settings/')
    else:
        form = MyChangeSettingsForm()
    return render_to_response('settings_page.html',
                              {'change_settings_form': form},
                              RequestContext(request))


@login_required
def my_validate_email(request, code):
    validation_code = code
    profile = UserProfile.objects.get(user=request.user)
    if validation_code != profile.validation_code:
        return HttpResponseRedirect('/')  # error page
    request.user.is_active = True
    request.user.save()

    return HttpResponseRedirect('/gradebook/overview/')


@login_required
def my_change_password(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.POST)

        if form.is_valid():
            if not request.user.check_password(form.cleaned_data.get('old_password')):
                errors = form.errors.setdefault('old_password', ErrorList())
                errors.append(form.error_messages['password_incorrect'])
            else:
                password1 = form.cleaned_data.get('new_password1')
                #password2 = form.cleaned_data.get('new_password2')
                #if password1 != password2:
                #    form.errors.setdefault('new_password1',
                #                           ErrorList()).append(form.error_messages['password_mismatch'])
                #else:
                request.user.set_password(password1)
                request.user.save()
                return HttpResponseRedirect('/account/settings/')
    else:
        form = MyPasswordChangeForm()
    return render_to_response('change_password_page.html',
                              {'password_change_form': form},
                              RequestContext(request))


def my_forgot_password_email(request):
    if request.method == 'POST':
        form = MyPasswordResetFormEmail(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            send_forgotten_password_email(email)
            return HttpResponseRedirect('/')
    else:
        form = MyPasswordResetFormEmail()
    return render_to_response('reset_password_page_email.html',
                              {'password_reset_form_email': form},
                              RequestContext(request))


def my_forgot_password_passwords(request, code):
    prof = UserProfile.objects.get(validation_code=code)
    if prof is None:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = MyPasswordResetFormPasswords(request.POST)

        if form.is_valid():
            password1 = form.cleaned_data.get('new_password1')
            password2 = form.cleaned_data.get('new_password2')
            if password1 != password2:
                form.errors.setdefault('new_password1', ErrorList()).append(form.error_messages['password_mismatch'])
            else:
                print('new pass: ' + password1)
                prof.user.set_password(password1)
                prof.user.save()
                login(request, authenticate(username=prof.user.email, password=password1))
                return HttpResponseRedirect('/account/settings/')
    else:
        form = MyPasswordResetFormPasswords()
    return render_to_response('reset_password_page_passwords.html',
                              {'password_reset_form_passwords': form,
                               'validation_code': code,
                               'user_email': prof.user.email},
                              RequestContext(request))


def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def send_validation_email(user):
    validation_code = ''.join(choice(ascii_letters + digits) for x in range(20))
    prof = UserProfile.objects.get(user=user)
    prof.validation_code = validation_code
    prof.save()

    subject = 'mygrades Validation Email'
    message = 'Hello ' + user.first_name + ' ' + user.last_name + ',\n\n'\
              'Thank you for registering with mygrades.\n' \
              'To get started, validate your email by clicking the following link.\n\n' + \
              BASE_PATH + '/account/validate_email/' + validation_code + '/\n'
    message = EmailMessage(subject, message, EMAIL_HOST_USER, [user.email])
    message.send(fail_silently=True)


def send_forgotten_password_email(email):
    validation_code = ''.join(choice(ascii_letters + digits) for x in range(20))
    user = User.objects.get(username=email)
    prof = UserProfile.objects.get(user=user)
    prof.validation_code = validation_code
    prof.save()

    subject = 'mygrades Forgot Password'
    message = 'Hello ' + user.first_name + ' ' + user.last_name + ',\n\n'\
              'You are receiving this email because you claimed to have forgotten your password on mygrades.\n' \
              'If this is a mistake, ignore this email. Else, follow the link below to reset your password.\n\n' + \
              BASE_PATH + '/account/forgot_password/' + validation_code + '/\n'
    message = EmailMessage(subject, message, EMAIL_HOST_USER, [user.email])
    message.send()

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.util import ErrorList
from django.core.mail import EmailMessage
from account.forms import MyLoginForm, MyUserCreationForm, MyChangeSettingsForm, MyPasswordChangeForm
from mygrades.settings import EMAIL_HOST_USER
from random import choice
from string import ascii_letters, digits
from account.models import UserProfile


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
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                form.errors.setdefault('password1', ErrorList()).append(form.error_messages['password_mismatch'])
            else:
                email = form.cleaned_data.get('email')
                user = User.objects.create_user(username=email,
                                                password=password1,
                                                email=email)
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.is_active = False  # user is inactive until email is validated
                prof = UserProfile(user=user)
                prof.save()
                user.save()

                send_validation_email(user)

                login(request, authenticate(username=email, password=password1))

                return HttpResponseRedirect('/gradebook/overview/')
    else:
        form = MyUserCreationForm()
    return render_to_response('signup_page.html',
                              {'signup_form': form},
                              RequestContext(request))


def send_validation_email(user):
    validation_code = ''.join(choice(ascii_letters + digits) for x in range(20))
    prof = UserProfile.objects.get(user=user)
    prof.validation_code = validation_code
    prof.save()

    subject = 'mygrades Validation Email'
    message = 'Thank you for registering with mygrades.\nTo get started, validate your' \
              'email by clicking the link below and entering the following code:\n' \
              '\nhttp://127.0.0.1:7654/account/settings/\n' + validation_code
    message = EmailMessage(subject, message, EMAIL_HOST_USER, [user.email])
    message.send()


@login_required
def my_settings(request):
    if request.method == 'POST':
        form = MyChangeSettingsForm(request.POST)

        if form.is_valid():
            validation_code = form.cleaned_data.get('validation_code')
            profile = UserProfile.objects.get(user=request.user)
            print(profile.validation_code)
            if validation_code != 'Validation Code' and validation_code.strip() != '' \
                and validation_code == profile.validation_code:
                    request.user.is_active = True
            else:
                form.errors.setdefault('validation_code', ErrorList()).append(form.error_messages['incorrect_validation'])

            email = form.cleaned_data.get('email')
            if email != 'Email' and email.strip() != '':
                request.user.username = email.strip()
                request.user.email = email.strip()
                request.user.is_active = False
                send_validation_email(request.user)

            first_name = form.cleaned_data.get('first_name')
            if first_name != 'First Name' and first_name.strip() != '':
                request.user.first_name = first_name.strip()

            last_name = form.cleaned_data.get('last_name')
            if last_name != 'Last Name' and last_name.strip() != '':
                request.user.last_name = last_name.strip()

            request.user.save()

            return HttpResponseRedirect('/account/settings/')
    else:
        form = MyChangeSettingsForm()
    return render_to_response('settings_page.html',
                              {'change_settings_form': form},
                              RequestContext(request))


@login_required
def my_change_password(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.POST)

        if form.is_valid():
            print('old pass: ' + form.cleaned_data.get('old_password'))
            if not request.user.check_password(form.cleaned_data.get('old_password')):
                errors = form.errors.setdefault('old_password', ErrorList())
                errors.append(form.error_messages['password_incorrect'])
            else:
                password1 = form.cleaned_data.get('new_password1')
                password2 = form.cleaned_data.get('new_password2')
                if password1 != password2:
                    form.errors.setdefault('new_password1', ErrorList()).append(form.error_messages['password_mismatch'])
                else:
                    print('new pass: ' + password1)
                    request.user.set_password(password1)
                    request.user.save()
                    return HttpResponseRedirect('/account/settings/')
    else:
        form = MyPasswordChangeForm()
    return render_to_response('change_password_page.html',
                              {'password_change_form': form},
                              RequestContext(request))


def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

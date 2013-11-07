from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from mygrades.forms import UserCreateForm
from django.contrib.auth.models import User


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

            return HttpResponseRedirect('/gradebook/report-card')
        return HttpResponseRedirect('/')
    return Http404


def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/gradebook/report-card/')
        else:
            return HttpResponseRedirect('/')

    return Http404


def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
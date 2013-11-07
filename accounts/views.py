from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404


def my_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password = password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/gradebook/report-card/')
        else:
            return HttpResponseRedirect('/')

    return Http404
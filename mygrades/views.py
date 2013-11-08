from django.shortcuts import render_to_response
from django.template import RequestContext
from account.forms import UserCreateForm, LoginForm


def home(request):
    return render_to_response('home.html', RequestContext(request))


def about(request):
    return render_to_response('about.html', RequestContext(request))


def base_form_context_processor(request):
    return {'login_form': LoginForm, 'signup_form': UserCreateForm}
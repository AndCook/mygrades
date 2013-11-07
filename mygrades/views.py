from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from mygrades.forms import UserCreateForm

def home(request):
    return render_to_response('home.html', RequestContext(request))

def about(request):
    return render_to_response('about.html', RequestContext(request))

def base_form_context_processor(request):
    return {'login_form': AuthenticationForm, 'signup_form': UserCreateForm}
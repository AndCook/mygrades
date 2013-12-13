from django.shortcuts import render_to_response
from django.template import RequestContext
from account.forms import MyUserCreationForm, MyLoginForm


def home(request):
    return render_to_response('home.html', RequestContext(request))


def about(request):
    return render_to_response('about.html', RequestContext(request))


def methodology(request):
    return render_to_response('methodology.html', RequestContext(request))


def contact_us(request):
    return render_to_response('contact_us.html', RequestContext(request))


def base_form_context_processor(request):
    last_name_initial = ''
    if request.user.is_authenticated() and len(request.user.last_name) > 0:
        last_name_initial = str(request.user.last_name[0])
    return {'login_form': MyLoginForm,
            'signup_form': MyUserCreationForm,
            'last_name_initial': last_name_initial}
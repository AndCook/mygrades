from django.shortcuts import render_to_response
from django.template import RequestContext
from account.forms import MyUserCreationForm, MyLoginForm
from django.http import HttpResponse
import json
from django.core.mail import EmailMessage
from mygrades.settings import EMAIL_HOST_USER


def home(request):
    return render_to_response('home.html', RequestContext(request))


def about(request):
    return render_to_response('about.html', RequestContext(request))


def methodology(request):
    return render_to_response('methodology.html', RequestContext(request))


def contact_us(request):
    if request.method == 'GET':
        return render_to_response('contact_us.html', RequestContext(request))

    if request.is_ajax():
        post_action = request.POST['post_action']
        if post_action == 'submit_comment':
            name = request.POST['name']
            email = request.POST['email']
            comment = request.POST['comment']
            subject = 'Comment from ' + name
            message = comment + '\n\n' + name + '\n' + email
            message = EmailMessage(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
            message.send(fail_silently=True)
            return HttpResponse(json.dumps({}), mimetype='application/json')


def base_form_context_processor(request):
    last_name_initial = ''
    if request.user.is_authenticated() and len(request.user.last_name) > 0:
        last_name_initial = str(request.user.last_name[0])
    return {'login_form': MyLoginForm,
            'signup_form': MyUserCreationForm,
            'last_name_initial': last_name_initial}
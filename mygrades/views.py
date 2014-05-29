from django.shortcuts import render_to_response
from django.template import RequestContext
from account.forms import MyUserCreationForm, MyLoginForm
from django.http import HttpResponse
import json
from django.core.mail import EmailMessage
from mygrades.settings import EMAIL_HOST_USER


# list of mobile User Agents
mobile_uas = ['w3c ', 'acs-', 'alav', 'alca', 'amoi', 'audi', 'avan', 'benq', 'bird', 'blac',
              'blaz', 'brew', 'cell', 'cldc', 'cmd-', 'dang', 'doco', 'eric', 'hipt', 'inno',
              'ipaq', 'java', 'jigs', 'kddi', 'keji', 'leno', 'lg-c', 'lg-d', 'lg-g', 'lge-',
              'maui', 'maxo', 'midp', 'mits', 'mmef', 'mobi', 'mot-', 'moto', 'mwbp', 'nec-',
              'newt', 'noki', 'oper', 'palm', 'pana', 'pant', 'phil', 'play', 'port', 'prox',
              'qwap', 'sage', 'sams', 'sany', 'sch-', 'sec-', 'send', 'seri', 'sgh-', 'shar',
              'sie-', 'siem', 'smal', 'smar', 'sony', 'sph-', 'symb', 't-mo', 'teli', 'tim-',
              'tosh', 'tsm-', 'upg1', 'upsi', 'vk-v', 'voda', 'wap-', 'wapa', 'wapi', 'wapp',
              'wapr', 'webc', 'winw', 'winw', 'xda', 'xda-']

mobile_ua_hints = ['SymbianOS', 'Opera Mini', 'iPhone']


def mobile_browser(request):
    # Super simple device detection, returns True for mobile devices

    is_mobile = False
    ua = request.META['HTTP_USER_AGENT'].lower()[0:4]

    if ua in mobile_uas:
        is_mobile = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                is_mobile = True

    return is_mobile


def home(request):
    if mobile_browser(request):
        template = 'm_home.html'
    else:
        template = 'home.html'
    return render_to_response(template, RequestContext(request))


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
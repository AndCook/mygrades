from django.shortcuts import render_to_response
from gradebook.models import Semester, Course, Category, Assignment
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import json


@csrf_protect
@login_required
def overview(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/account/settings/')

    if request.method == 'GET':
        semesters = Semester.objects.filter(user=request.user)
        for semester in semesters:
            courses = Course.objects.filter(semester=semester)
            semester.courses = courses
        return render_to_response('overview.html',
                                  {'semesters': semesters},
                                  RequestContext(request))

    if request.is_ajax():
        post_action = request.POST['post_action']
        if post_action == 'create_semester':
            new_semester_name = request.POST['new_semester_name']
            semester = Semester(name=new_semester_name, user=request.user)
            semester.save()
            return_dict = {'id': semester.id}
            js = json.dumps(return_dict)
            return HttpResponse(js, mimetype='application/json')
        elif post_action == 'delete_semester':
            # id is of form "semester_23" and we need just number
            delete_semester_id = request.POST['delete_semester_id']
            semesters = Semester.objects.filter(id=delete_semester_id)
            if semesters.__len__() == 1:
                semesters[0].delete()
            return HttpResponse(json.dumps({}), mimetype='application/json')
        elif post_action == 'rename_semester':
            rename_semester_id = request.POST['rename_semester_id']
            new_semester_name = request.POST['new_semester_name']
            semesters = Semester.objects.filter(id=rename_semester_id)
            if semesters.__len__() == 1:
                semesters[0].name = new_semester_name
                semesters[0].save()
            return HttpResponse(json.dumps({}), mimetype='application/json')
        elif post_action == 'add_course':
            new_course_name = request.POST['new_course_name']
            semester_id = request.POST['semester_id']
            semester = Semester.objects.filter(id=semester_id)
            if semester.__len__() == 1:
                course = Course(name=new_course_name, number='XXXXX',
                                instructor='Dr. X', semester=semester[0])
                course.save()
                return HttpResponse(json.dumps({}), mimetype='application/json')


@login_required
def semester_detail(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/account/settings/')

    return render_to_response('semester_detail.html', RequestContext(request))


@login_required
def course_detail(request, course_id):
    if not request.user.is_active:
        return HttpResponseRedirect('/account/settings/')

    courses = Course.objects.filter(id=course_id)
    # make sure course_id is valid
    if courses.__len__() != 1:
        return Http404()
    course = courses[0]
    semester = course.semester
    # make sure current user has access to requested course
    if request.user != semester.user:
        return Http404

    return render_to_response('course_detail.html',
                              {'course': course},
                              RequestContext(request))
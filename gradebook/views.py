from django.shortcuts import render_to_response
from gradebook.models import Semester, SemesterForm, Course, CourseForm, Category, Assignment
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import json
from datetime import datetime, date


@csrf_protect
@login_required
def overview(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/account/settings/')

    if request.method == 'GET':
        semesters = Semester.objects.filter(user=request.user)
        semesters = semesters.order_by('start_date')
        for semester in semesters:
            start_date = semester.start_date
            end_date = semester.end_date
            current_date = date.today()
            semester.is_future = current_date < start_date <= end_date
            semester.is_current = start_date <= current_date <= end_date
            semester.is_finished = start_date <= end_date < current_date
            semester.save()
            semester.courses = Course.objects.filter(semester=semester)
        return render_to_response('overview.html',
                                  {'semesters': semesters,
                                   'semester_form': SemesterForm(),
                                   'course_form': CourseForm()},
                                  RequestContext(request))

    if request.is_ajax():
        post_action = request.POST['post_action']
        if post_action == 'add_semester':
            semester_name = request.POST['semester_name']
            start_date_string = request.POST['start_date']
            if start_date_string != '':
                start_date = datetime.strptime(start_date_string, '%b %d, %Y')
            else:
                start_date = datetime.today()
            end_date_string = request.POST['end_date']
            if end_date_string != '':
                end_date = datetime.strptime(end_date_string, '%b %d, %Y')
            else:
                end_date = datetime.today()
            semester = Semester(name=semester_name, user=request.user,
                                start_date=start_date, end_date=end_date)
            current_date = datetime.today()
            semester.is_future = (current_date < start_date <= end_date)
            semester.is_current = (start_date <= current_date <= end_date)
            semester.is_finished = (start_date <= end_date < current_date)
            semester.save()
            return render_to_response('semester_square.html', {'semester': semester}, RequestContext(request))
        elif post_action == 'rename_semester':
            semester_id = request.POST['semester_id']
            new_semester_name = request.POST['new_semester_name']
            semesters = Semester.objects.filter(id=semester_id)
            if semesters.__len__() == 1:
                semesters[0].name = new_semester_name
                semesters[0].save()
            return HttpResponse(json.dumps({}), mimetype='application/json')
        elif post_action == 'delete_semester':
            semester_id = request.POST['semester_id']
            semesters = Semester.objects.filter(id=semester_id)
            if semesters.__len__() == 1:
                semesters[0].delete()
            return HttpResponse(json.dumps({}), mimetype='application/json')
        elif post_action == 'change_dates':
            semester_id = request.POST['semester_id']
            semesters = Semester.objects.filter(id=semester_id)
            if semesters.__len__() == 1:
                semester = semesters[0]
                new_start_date_string = request.POST['new_start_date']
                if new_start_date_string != '':
                    semester.start_date = datetime.strptime(new_start_date_string, '%b %d, %Y')
                new_end_date_string = request.POST['new_end_date']
                if new_end_date_string != '':
                    semester.end_date = datetime.strptime(new_end_date_string, '%b %d, %Y')
                current_date = datetime.today()
                start_date = semester.start_date
                end_date = semester.end_date
                semester.is_future = (current_date < start_date <= end_date)
                semester.is_current = (start_date <= current_date <= end_date)
                semester.is_finished = (start_date <= end_date < current_date)
                semester.save()
                semester.courses = Course.objects.filter(semester=semester)
                return render_to_response('semester_square.html', {'semester': semester}, RequestContext(request))
            return HttpResponse(json.dumps({}), mimetype='application/json')
        elif post_action == 'add_course':
            course_name = request.POST['course_name']
            course_number = request.POST['course_number']
            course_instructor = request.POST['course_instructor']
            course_hours = request.POST['course_hours']
            semester_id = request.POST['semester_id']
            semesters = Semester.objects.filter(id=semester_id)
            if semesters.__len__() == 1:
                course = Course(name=course_name, number=course_number,
                                instructor=course_instructor, hours=course_hours,
                                semester=semesters[0])
                course.save()
                return render_to_response('course_table_row.html', {'course': course}, RequestContext(request))
        elif post_action == 'edit_course':
            course_id = request.POST['course_id']
            courses = Course.objects.filter(id=course_id)
            if courses.__len__() == 1:
                course = courses[0]
                course.name = request.POST['course_name']
                course.number = request.POST['course_number']
                course.instructor = request.POST['course_instructor']
                course.hours = request.POST['course_hours']
                course.save()
                return render_to_response('course_table_row.html', {'course': course}, RequestContext(request))
        elif post_action == 'delete_course':
            course_id = request.POST['course_id']
            courses = Course.objects.filter(id=course_id)
            if courses.__len__() == 1:
                courses[0].delete()
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
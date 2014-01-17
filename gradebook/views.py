from django.shortcuts import render_to_response
from gradebook.models import Semester, SemesterForm, Course, CourseForm
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import json
from datetime import datetime, date
from gradebook.models import letter_grade_to_gpa_points, PASSING_GRADES, GPA_GRADES
#from account.models import User


@csrf_protect
@login_required
def overview(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/account/settings/')

    if request.method == 'GET':
        #for semester in Semester.objects.all():
        #    recount_hours(semester)
        #for user in User.objects.all():  # import User from account.models
        #    recalculate_cumulative_gpa(user)

        semesters = Semester.objects.filter(user=request.user)
        semesters = semesters.order_by('start_date')
        for semester in semesters:
            if not semester.is_finished:
                recheck_semester_dates(semester)
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
            recheck_semester_dates(semester)  # semester.save included in method
            recalculate_cumulative_gpa(request.user)
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
                recheck_semester_dates(semester)  # semester.save included in method
                recalculate_cumulative_gpa(request.user)
                semester.courses = Course.objects.filter(semester=semester)
                return render_to_response('semester_square.html', {'semester': semester}, RequestContext(request))
            return HttpResponse(json.dumps({}), mimetype='application/json')
        elif post_action == 'add_course':
            course_name = request.POST['course_name']
            course_number = request.POST['course_number']
            course_instructor = request.POST['course_instructor']
            course_hours = int(request.POST['course_hours'])
            semester_id = request.POST['semester_id']
            semesters = Semester.objects.filter(id=semester_id)
            if semesters.__len__() == 1:
                course = Course(name=course_name, number=course_number,
                                instructor=course_instructor, hours=course_hours,
                                semester=semesters[0])
                course.save()
                course.semester.hours_planned += course.hours
                course.semester.save()
                course.semester.courses = Course.objects.filter(semester=course.semester)
                return render_to_response('semester_square.html',
                                          {'semester': course.semester},
                                          RequestContext(request))
            return HttpResponse(json.dumps({}), mimetype='application/json')
        elif post_action == 'edit_course':
            course_id = request.POST['course_id']
            courses = Course.objects.filter(id=course_id)
            if courses.__len__() == 1:
                course = courses[0]
                course.name = request.POST['course_name']
                course.number = request.POST['course_number']
                course.instructor = request.POST['course_instructor']

                course.semester.hours_planned -= course.hours
                if course.final_grade in PASSING_GRADES:
                    course.semester.hours_passed -= course.hours
                if course.final_grade in GPA_GRADES:
                    course.semester.gpa_hours -= course.hours
                    course.semester.gpa_points -= course.gpa_points

                course.hours = int(request.POST['course_hours'])
                course.gpa_points = letter_grade_to_gpa_points(course.final_grade, course.hours)

                course.semester.hours_planned += course.hours
                if course.final_grade in PASSING_GRADES:
                    course.semester.hours_passed += course.hours
                if course.final_grade in GPA_GRADES:
                    course.semester.gpa_hours += course.hours
                    course.semester.gpa_points += course.gpa_points
                    if course.semester.gpa_hours != 0:
                        course.semester.final_gpa = round(course.semester.gpa_points / course.semester.gpa_hours, 3)
                    else:
                        course.semester.final_gpa = -1.0

                course.semester.save()
                course.save()
                recalculate_cumulative_gpa(request.user)
                course.semester.courses = Course.objects.filter(semester=course.semester)
                return render_to_response('semester_square.html',
                                          {'semester': course.semester},
                                          RequestContext(request))
            return HttpResponse(json.dumps({}), mimetype='application/json')
        elif post_action == 'delete_course':
            course_id = request.POST['course_id']
            courses = Course.objects.filter(id=course_id)
            if courses.__len__() == 1:
                course = courses[0]
                course.semester.hours_planned -= course.hours
                if course.final_grade in PASSING_GRADES:
                    course.semester.hours_passed -= course.hours
                if course.final_grade in GPA_GRADES:
                    course.semester.gpa_hours -= course.hours
                    course.semester.gpa_points -= course.gpa_points
                    if course.semester.gpa_hours != 0:
                        course.semester.final_gpa = round(course.semester.gpa_points / course.semester.gpa_hours, 3)
                    else:
                        course.semester.final_gpa = -1.0

                course.semester.save()
                recalculate_cumulative_gpa(request.user)
                course.delete()
                course.semester.courses = Course.objects.filter(semester=course.semester)
                return render_to_response('semester_square.html',
                                          {'semester': course.semester},
                                          RequestContext(request))
            return HttpResponse(json.dumps({}), mimetype='application/json')


def recheck_semester_dates(semester):
    start_date = semester.start_date
    end_date = semester.end_date
    if type(end_date) is type(datetime(day=1, month=1, year=1)):
        current_date = datetime.today()
    else:
        current_date = date.today()
    semester.is_future = (current_date < start_date <= end_date)
    semester.is_current = start_date <= current_date <= end_date
    semester.is_finished = start_date <= end_date < current_date
    semester.save()


def recount_hours(semester):
    course_list = Course.objects.filter(semester=semester)
    semester.hours_planned = 0
    semester.hours_passed = 0
    semester.gpa_hours = 0
    semester.gpa_points = 0
    for course in course_list:
        semester.hours_planned += course.hours
        if course.final_grade in PASSING_GRADES:
            semester.hours_passed += course.hours
        if course.final_grade in GPA_GRADES:
            semester.gpa_hours += course.hours
            semester.gpa_points += course.gpa_points
    if semester.gpa_hours != 0:
        semester.final_gpa = round(semester.gpa_points / semester.gpa_hours, 3)
    else:
        semester.final_gpa = -1.0
    semester.save()


def recalculate_cumulative_gpa(user):
    cumulative_hours_passed = 0
    cumulative_gpa_hours = 0
    cumulative_gpa_points = 0
    for semester in Semester.objects.filter(user=user, is_finished=True).order_by('start_date'):
        cumulative_hours_passed += semester.hours_passed
        cumulative_gpa_hours += semester.gpa_hours
        cumulative_gpa_points += semester.gpa_points
        if cumulative_gpa_hours != 0:
            semester.cumulative_gpa = round(cumulative_gpa_points / cumulative_gpa_hours, 3)
        else:
            semester.cumulative_gpa = -1.0
        semester.cumulative_hours_passed = cumulative_hours_passed
        semester.save()
    for semester in Semester.objects.filter(user=user, is_finished=False).order_by('start_date'):
        cumulative_hours_passed += semester.hours_planned
        semester.cumulative_hours_passed = cumulative_hours_passed
        semester.save()


@login_required
def course_detail(request, course_id):
    if not request.user.is_active:
        return HttpResponseRedirect('/account/settings/')

    if request.method == 'GET':
        courses = Course.objects.filter(id=course_id)
        # make sure course_id is valid
        if courses.__len__() != 1:
            return Http404()
        course = courses[0]
        semester = course.semester
        # make sure current user has access to requested course
        if request.user != semester.user:
            return Http404()

        course.semester.courses = Course.objects.filter(semester=course.semester)
        return render_to_response('course_detail.html',
                                  {'course': course,
                                   'course_form': CourseForm()},
                                  RequestContext(request))

    if request.is_ajax():
        post_action = request.POST['post_action']
        if post_action == 'report_final_grade':
            courses = Course.objects.filter(id=course_id)
            if courses.__len__() == 1:
                course = courses[0]

                if course.final_grade in PASSING_GRADES:
                    course.semester.hours_passed -= course.hours
                if course.final_grade in GPA_GRADES:
                    course.semester.gpa_hours -= course.hours
                    course.semester.gpa_points -= course.gpa_points

                course.final_grade = request.POST['final_grade']
                course.gpa_points = letter_grade_to_gpa_points(course.final_grade, course.hours)

                if course.final_grade in PASSING_GRADES:
                    course.semester.hours_passed += course.hours
                if course.final_grade in GPA_GRADES:
                    course.semester.gpa_hours += course.hours
                    course.semester.gpa_points += course.gpa_points
                if course.semester.gpa_hours != 0:
                    course.semester.final_gpa = round(course.semester.gpa_points / course.semester.gpa_hours, 3)
                else:
                    course.semester.final_gpa = -1.0

                course.semester.save()
                course.save()
                recalculate_cumulative_gpa(request.user)
            return HttpResponse(json.dumps({}), mimetype='application/json')

from django.shortcuts import render_to_response
from gradebook.models import Semester, SemesterForm, Course, CourseForm, Category, Assignment
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
import json
from datetime import datetime
from gradebook.models import sanity_check_all, recalculate_cumulative_gpa
from django.shortcuts import get_object_or_404


@csrf_protect
def overview(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if not request.user.is_active:
        return HttpResponseRedirect('/account/settings/')

    if request.method == 'GET':
        # sanity_check_all()

        semesters = request.user.semester_set
        semesters = semesters.order_by('start_date')
        for semester in semesters:
            if not semester.is_finished:
                semester.recheck_dates()
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
            semester.recheck_dates()  # save included
            recalculate_cumulative_gpa(request.user)
            return render_to_response('semester_square.html', {'semester': semester}, RequestContext(request))
        elif post_action == 'rename_semester':
            new_semester_name = request.POST['new_semester_name']
            semester = Semester.objects.get(id=request.POST['semester_id'])
            semester.name = new_semester_name
            semester.save()
            return HttpResponse(json.dumps({}), mimetype='application/json')
        elif post_action == 'delete_semester':

            Semester.objects.get(id=request.POST['semester_id']).delete()
            recalculate_cumulative_gpa(request.user)

            return HttpResponse(json.dumps({}), mimetype='application/json')
        elif post_action == 'change_dates':
            semester_id = request.POST['semester_id']
            semester = Semester.objects.get(id=semester_id)
            new_start_date_string = request.POST['new_start_date']
            if new_start_date_string != '':
                semester.start_date = datetime.strptime(new_start_date_string, '%b %d, %Y')
            new_end_date_string = request.POST['new_end_date']
            if new_end_date_string != '':
                semester.end_date = datetime.strptime(new_end_date_string, '%b %d, %Y')
            semester.recheck_dates()  # save included
            recalculate_cumulative_gpa(request.user)
            return render_to_response('semester_square.html', {'semester': semester}, RequestContext(request))
        elif post_action == 'add_course':
            course = Course(name=request.POST['course_name'],
                            number=request.POST['course_number'],
                            instructor=request.POST['course_instructor'],
                            semester=Semester.objects.get(id=request.POST['semester_id']))
            course.set_hours(int(request.POST['course_hours']))  # save included

            return render_to_response('semester_square.html',
                                      {'semester': course.semester},
                                      RequestContext(request))
        elif post_action == 'edit_course':
            course = Course.objects.get(id=request.POST['course_id'])

            course.name = request.POST['course_name']
            course.number = request.POST['course_number']
            course.instructor = request.POST['course_instructor']

            course.set_hours(int(request.POST['course_hours']))  # save included

            recalculate_cumulative_gpa(request.user)

            return render_to_response('semester_square.html',
                                      {'semester': course.semester},
                                      RequestContext(request))
        elif post_action == 'delete_course':
            course = Course.objects.get(id=request.POST['course_id'])

            course.set_hours(0)  # save included
            course.delete()

            recalculate_cumulative_gpa(request.user)

            return render_to_response('semester_square.html',
                                      {'semester': course.semester},
                                      RequestContext(request))


@csrf_protect
def current_courses(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if not request.user.is_active:
        return HttpResponseRedirect('/account/settings/')

    if request.method == 'GET':
        semesters = request.user.semester_set
        semesters = semesters.order_by('start_date')
        for semester in semesters:
            if not semester.is_finished:
                semester.recheck_dates()
        semesters = semesters.filter(is_current=True)
        semesters = semesters.order_by('start_date')
        return render_to_response('current_courses.html',
                                  {'semesters': semesters,
                                   'semester_form': SemesterForm(),
                                   'course_form': CourseForm()},
                                  RequestContext(request))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


@csrf_protect
def course_detail(request, course_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if not request.user.is_active:
        return HttpResponseRedirect('/account/settings/')

    if request.method == 'GET':
        if request.is_ajax():
            get_action = request.GET['get_action']
            if get_action == 'add_category_size_check':
                course = Course.objects.get(id=course_id)
                worth = request.GET['worth']
                is_valid = is_number(worth) and float(worth) <= course.not_specified_worth
                return HttpResponse(json.dumps({'is_valid': is_valid}), mimetype='application/json')
            if get_action == 'edit_category_size_check':
                course = Course.objects.get(id=course_id)
                original_worth = request.GET['original_worth']
                new_worth = request.GET['new_worth']
                is_valid = is_number(original_worth) and is_number(new_worth) and \
                    float(new_worth) <= float(original_worth) + course.not_specified_worth
                return HttpResponse(json.dumps({'is_valid': is_valid}), mimetype='application/json')
            if get_action == 'add_category_name_unique':
                course = Course.objects.get(id=course_id)
                name = request.GET['name']
                cat_set = course.category_set.filter(name=name)
                is_unique = cat_set.__len__() == 0
                return HttpResponse(json.dumps({'is_unique': is_unique}), mimetype='application/json')
            if get_action == 'edit_category_name_unique':
                course = Course.objects.get(id=course_id)
                name = request.GET['name']
                cat_set = course.category_set.filter(name=name)
                is_unique = cat_set.__len__() == 0
                return HttpResponse(json.dumps({'is_unique': is_unique}), mimetype='application/json')
            if get_action == 'get_category_id':
                course = Course.objects.get(id=course_id)
                category = Category.objects.get(course=course, name=request.GET['category_name'])
                return HttpResponse(json.dumps({'category_id': category.id}), mimetype='application/json')
        ##### normal page load #####
        course = get_object_or_404(Course, id=course_id)
        # make sure current user has access to requested course
        if request.user != course.semester.user:
            return Http404()

        semesters = request.user.semester_set
        semesters = semesters.exclude(id=course.semester.id)
        return render_to_response('course_detail.html',
                                  {'course': course,
                                   'all_other_semesters': semesters,
                                   'course_form': CourseForm()},
                                  RequestContext(request))

    if request.is_ajax():
        post_action = request.POST['post_action']
        if post_action == 'report_final_grade':
            course = Course.objects.get(id=course_id)

            course.change_final_grade(request.POST['final_grade'])  # save included

            return HttpResponse(json.dumps({}), mimetype='application/json')
        if post_action == 'add_category':
            course = Course.objects.get(id=course_id)

            category = Category(name=request.POST['category_name'],
                                course=course, worth=0)
            category.set_worth(request.POST['category_worth'])  # save included

            return render_to_response('course_categories_assignments.html',
                                      {'course': course},
                                      RequestContext(request))
        if post_action == 'edit_category':
            category = Category.objects.get(id=request.POST['category_id'])
            category.name = request.POST['category_name']

            category.set_worth(float(request.POST['category_worth']))  # save included

            return render_to_response('course_categories_assignments.html',
                                      {'course': Course.objects.get(id=course_id)},
                                      RequestContext(request))
        if post_action == 'delete_category':
            category = Category.objects.get(id=request.POST['category_id'], course=Course.objects.get(id=course_id))

            category.set_worth(0)  # save included
            category.delete()

            return render_to_response('course_categories_assignments.html',
                                      {'course': category.course},
                                      RequestContext(request))
        if post_action == 'add_assignment':
            category = Category.objects.get(id=request.POST['assignment_category_id'])
            grade_unknown = request.POST['assignment_grade_unknown'] == u'true'
            assign = Assignment(name=request.POST['assignment_name'],
                                category=category,
                                grade_unknown=grade_unknown)
            if grade_unknown:
                points_earned = 0
            else:
                points_earned = float(request.POST['assignment_points_earned'])
            total_points = float(request.POST['assignment_total_points'])
            assign.set_points(grade_unknown, points_earned, total_points)  # save included

            return render_to_response('course_categories_assignments.html',
                                      {'course': Course.objects.get(id=course_id)},
                                      RequestContext(request))
        if post_action == 'edit_assignment':
            assign = Assignment.objects.get(id=request.POST['assignment_id'])
            assign.name = request.POST['new_name']
            category = Category.objects.get(id=request.POST['new_category_id'])
            if assign.category != category:
                assign.change_category(category)

            grade_unknown = request.POST['new_grade_unknown'] == u'true'
            if grade_unknown:
                points_earned = 0
            else:
                points_earned = float(request.POST['new_points_earned'])
            total_points = float(request.POST['new_total_points'])
            assign.set_points(grade_unknown, points_earned, total_points)  # save included

            return render_to_response('course_categories_assignments.html',
                                      {'course': Course.objects.get(id=course_id)},
                                      RequestContext(request))
        if post_action == 'delete_assignment':
            assign = Assignment.objects.get(id=request.POST['assignment_id'])

            assign.set_points(assign.grade_unknown, 0, 0)  # save included
            assign.delete()

            return render_to_response('course_categories_assignments.html',
                                      {'course': Course.objects.get(id=course_id)},
                                      RequestContext(request))
from django.shortcuts import render_to_response
from gradebook.models import Semester, Course, Category, Assignment
from django.http import HttpResponseRedirect, Http404


def report_card(request):
    return render_to_response('report-card.html')


def semester_overview(request):
    return render_to_response('semester-overview.html')


def course_detail(request):
    if request.user.is_authenticated():
        semesters = Semester.objects.all()
        selected_semester = None
        if len(semesters) > 0:
            selected_semester = semesters[0]
        courses = Course.objects.all()
        selected_course = None
        if len(courses) > 0:
            selected_course = courses[0]
        categories = Category.objects.filter(course=selected_course)
        for cat in categories:
            cat.assignments = Assignment.objects.filter(category=cat)
            cat.has_assignments = (len(cat.assignments) > 0)

        return render_to_response('course-detail.html',
                                  {'selected_semester': selected_semester,
                                   'semesters': semesters,
                                   'selected_course': selected_course,
                                   'courses': courses,
                                   'categories': categories})
    else:
        return Http404 # change to redirect to a login page
from django.shortcuts import render_to_response
from gradebook.models import Semester, Course, Category, Assignment
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def overview(request):
    return render_to_response('overview.html', RequestContext(request))

@login_required
def semester_detail(request):
    return render_to_response('semester_detail.html', RequestContext(request))

@login_required
def course_detail(request):
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

    return render_to_response('course_detail.html',
                              {'user': request.user,
                               'selected_semester': selected_semester,
                               'semesters': semesters,
                               'selected_course': selected_course,
                               'courses': courses,
                               'categories': categories})
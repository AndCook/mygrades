from django.shortcuts import render_to_response
from Gradebook.models import Semester, Course, Category, Assignment


def home(request):
    return render_to_response('home.html')


def report_card(request):
    return render_to_response('report-card.html')


def semester_overview(request):
    return render_to_response('semester-overview.html')


def course_detail(request):
    semesters = Semester.objects.all()
    courses = Course.objects.all()
    categories = Category.objects.filter(course=courses[0])
    for cat in categories:
        cat.assignments = Assignment.objects.filter(category=cat)
        cat.has_assignments = (len(cat.assignments) > 0)

    return render_to_response('course-detail.html',
                              {'selected_semester': semesters[0],
                               'semesters': semesters,
                               'selected_course': courses[0],
                               'courses': courses,
                               'categories': categories})

from django.shortcuts import render_to_response
from Gradebook.models import Semester, Course, Category, Assignment


def home(request):
    return render_to_response('home.html')


def report_card(request):
    return render_to_response('report-card.html')


def semester_overview(request):
    semesters = Semester.objects.all()
    courses = Course.objects.all()
    return render_to_response('semester-overview.html',
                              {'selected_semester': semesters[0],
                               'courses': courses})


def course_detail(request):
    courses = Course.objects.all()
    categories = Category.objects.all()
    assignments = Assignment.objects.all()

    return render_to_response('course-detail.html',
                              {'selected_course': courses[0],
                               'categories': categories,
                               'assignments': assignments})

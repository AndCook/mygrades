from gradebook.models import Semester, Course, Category, Assignment
from django.contrib import admin


class SemesterAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'start_date', 'end_date', 'is_finished', 'is_current', 'is_future',
                    'hours_planned', 'hours_passed', 'gpa_hours', 'gpa_points', 'final_gpa']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'name', 'hours', 'instructor', 'semester', 'final_grade', 'gpa_points']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'worth', 'course']


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'awardedPoints', 'possiblePoints', 'percentage', 'category']


admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Assignment, AssignmentAdmin)
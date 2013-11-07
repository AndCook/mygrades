from gradebook.models import Semester, Course, Category, Assignment
from django.contrib import admin


class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'instructor', 'semester']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'worth', 'course']


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'awardedPoints', 'possiblePoints', 'percentage', 'category']


admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Assignment, AssignmentAdmin)
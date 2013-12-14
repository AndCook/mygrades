from gradebook.models import Semester, Course, Category, Assignment
from django.contrib import admin


class SemesterAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'start_date', 'end_date']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'name', 'instructor', 'semester']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'worth', 'course']


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'awardedPoints', 'possiblePoints', 'percentage', 'category']


admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Assignment, AssignmentAdmin)
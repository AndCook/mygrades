from gradebook.models import Semester, Course, Category, Assignment
from django.contrib import admin


class SemesterAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'start_date', 'end_date', 'is_finished', 'is_current', 'is_future',
                    'hours_planned', 'hours_passed', 'gpa_hours', 'gpa_points', 'final_gpa',
                    'cumulative_gpa', 'cumulative_hours_passed']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'name', 'hours', 'instructor', 'semester', 'final_grade', 'gpa_points']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'worth', 'course',
                    'actual_points_earned', 'actual_total_points',
                    'category_percentage', 'category_weighted_percentage',
                    'max_points_earned', 'total_points',
                    'min_category_percentage', 'max_category_percentage',
                    'min_category_weighted_percentage', 'max_category_weighted_percentage']


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'grade_unknown',
                    'points_earned', 'total_points', 'percentage']


admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Assignment, AssignmentAdmin)
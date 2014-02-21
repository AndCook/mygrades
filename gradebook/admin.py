from gradebook.models import Semester, Course, Category, Assignment
from django.contrib import admin


class SemesterAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'start_date', 'end_date',
                    'is_finished', 'is_current', 'is_future',
                    'hours_planned', 'hours_passed', 'gpa_hours', 'final_grade_points', 'final_gpa',
                    'cumulative_gpa', 'cumulative_gpa_hours', 'cumulative_hours_passed',
                    'potential_min_grade_points', 'potential_grade_points', 'potential_max_grade_points',
                    'potential_hours_counted', 'potential_min_gpa', 'potential_gpa', 'potential_max_gpa']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'name', 'hours', 'instructor', 'semester',
                    'final_grade', 'final_grade_points',
                    'not_specified_worth',
                    'total_weighted_percentage', 'total_worth_used', 'course_grade',
                    'course_min_grade', 'course_max_grade',
                    'course_grade_points', 'course_min_grade_points', 'course_max_grade_points']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'worth', 'course',
                    'actual_points_earned', 'actual_total_points',
                    'category_percentage', 'category_weighted_percentage',
                    'max_points_earned', 'total_points',
                    'category_percentage', 'category_weighted_percentage',
                    'min_category_percentage', 'min_category_weighted_percentage',
                    'max_category_percentage', 'max_category_weighted_percentage']


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'grade_unknown',
                    'points_earned', 'total_points', 'percentage']


admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Assignment, AssignmentAdmin)
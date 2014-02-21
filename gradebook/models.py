from django.db import models
from django.contrib.auth.models import User
from django import forms
import datetime


class Semester(models.Model):
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User, default=None)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)

    is_finished = models.BooleanField(default=False)
    is_current = models.BooleanField(default=False)
    is_future = models.BooleanField(default=False)

    hours_planned = models.IntegerField(default=0)
    hours_passed = models.IntegerField(default=0)
    gpa_hours = models.IntegerField(default=0)
    final_grade_points = models.FloatField(default=0)
    final_gpa = models.FloatField(default=0)

    cumulative_gpa = models.FloatField(default=0)
    cumulative_gpa_hours = models.FloatField(default=0)
    cumulative_hours_passed = models.IntegerField(default=0)

    potential_min_grade_points = models.FloatField(default=0)
    potential_grade_points = models.FloatField(default=0)
    potential_max_grade_points = models.FloatField(default=0)
    potential_hours_counted = models.FloatField(default=0)
    potential_min_gpa = models.FloatField(default=0)
    potential_gpa = models.FloatField(default=0)
    potential_max_gpa = models.FloatField(default=0)

    def recheck_dates(self):
        start_date = self.start_date
        end_date = self.end_date
        if type(end_date) is type(datetime.datetime(day=1, month=1, year=1)):
            current_date = datetime.datetime.today()
        else:
            current_date = datetime.date.today()
        self.is_future = (current_date < start_date <= end_date)
        self.is_current = start_date <= current_date <= end_date
        self.is_finished = start_date <= end_date < current_date
        self.save()

    ### THIS METHOD SHOULD NEVER BE CALLED WITHOUT AN ACCOMPYING add_course() AFTER IT
    ### These methods are used in pair by Assignment.set_point() and Assignment.change_category()
    ###     and Category.set_worth() and Course.set_hours() and Course.set_final_grade()
    def remove_course(self, course):
        print '6'
        ### Remove course from current semester
        self.hours_planned -= course.hours
        if course.final_grade in PASSING_GRADES:
            self.hours_passed -= course.hours
        if course.final_grade in GPA_GRADES:
            self.gpa_hours -= course.hours
        self.final_grade_points -= course.final_grade_points
        if course.final_grade != '#':
            self.potential_min_grade_points -= course.final_grade_points
            self.potential_grade_points -= course.final_grade_points
            self.potential_max_grade_points -= course.final_grade_points
            self.potential_hours_counted -= course.hours
        elif course.total_worth_used != 0:
            self.potential_min_grade_points -= course.course_min_grade_points
            self.potential_grade_points -= course.course_grade_points
            self.potential_max_grade_points -= course.course_max_grade_points
            self.potential_hours_counted -= course.hours
        ### Return without saving since that is done in add_course
        print '6.5'

    def add_course(self, course):
        print '7'
        ### Add course back to current semester
        self.hours_planned += course.hours
        if course.final_grade in PASSING_GRADES:
            self.hours_passed += course.hours
        if course.final_grade in GPA_GRADES:
            self.gpa_hours += course.hours
        self.final_grade_points += course.final_grade_points
        if course.final_grade != '#':
            self.potential_min_grade_points += course.final_grade_points
            self.potential_grade_points += course.final_grade_points
            self.potential_max_grade_points += course.final_grade_points
            self.potential_hours_counted += course.hours
        elif course.total_worth_used != 0:
            self.potential_min_grade_points += course.course_min_grade_points
            self.potential_grade_points += course.course_grade_points
            self.potential_max_grade_points += course.course_max_grade_points
            self.potential_hours_counted += course.hours
        ### Calculate current semester's gpa'sif semester.final_grade_points == 0:
        self.final_gpa = 0
        if self.final_grade_points == 0:
            self.final_gpa = 0
        else:
            self.final_gpa = self.final_grade_points / self.gpa_hours
        if self.potential_hours_counted == 0:
            self.potential_min_gpa = 0
            self.potential_gpa = 0
            self.potential_max_gpa = 0
        else:
            self.potential_min_gpa = self.potential_min_grade_points / self.potential_hours_counted
            self.potential_gpa = self.potential_grade_points / self.potential_hours_counted
            self.potential_max_gpa = self.potential_max_grade_points / self.potential_hours_counted
        ### Recalculate cumulative gpa's
        recalculate_cumulative_gpa(self.user)
        ### Save current semester and return
        self.save()
        print '7.5'

    def __unicode__(self):
        return self.name


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name', 'start_date', 'end_date']
        widgets = {'name': forms.TextInput(attrs={'autocomplete': 'off'}),
                   'start_date': forms.DateInput(format='%b %d, %Y',
                                                 attrs={'class': 'start_date_input'}),
                   'end_date': forms.DateInput(format='%b %d, %Y',
                                               attrs={'class': 'end_date_input'})
                   }

NONE_YET = '#'
GRADE_CHOICES = (
    (NONE_YET, 'None Yet'),
    ('A+', 'A+'),
    ('A', 'A'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B', 'B'),
    ('B-', 'B-'),
    ('C+', 'C+'),
    ('C', 'C'),
    ('C-', 'C-'),
    ('D+', 'D+'),
    ('D', 'D'),
    ('D-', 'D-'),
    ('F', 'F'),
    ('CR', 'Credit'),
    ('NC', 'No Credit'),
    ('P', 'Pass'),
    ('FL', 'Fail'),
    ('W', 'Withdrawl')
)
PASSING_GRADES = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'CR', 'P']
GPA_GRADES = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']


def letter_grade_to_grade_points(letter_grade, hours):
    grade_points = 0
    if letter_grade[0] == 'A':
        grade_points = 4
    elif letter_grade[0] == 'B':
        grade_points = 3
    elif letter_grade[0] == 'C':
        grade_points = 2
    elif letter_grade[0] == 'D':
        grade_points = 1
    if len(str(letter_grade)) == 2:
        if letter_grade[1] == '+':
            grade_points += 0.33
        elif letter_grade[1] == '-':
            grade_points -= 0.33
        else:  # to account for CR
            grade_points = 0
    return grade_points * hours


def percentage_grade_to_grade_points(percent, hours):
    grade_points = 0
    if percent >= 93:
        grade_points = 4
    elif percent >= 90:
        grade_points = 3.66
    elif percent >= 87:
        grade_points = 3.33
    elif percent >= 83:
        grade_points = 3
    elif percent >= 80:
        grade_points = 2.66
    elif percent >= 77:
        grade_points = 2.33
    elif percent >= 73:
        grade_points = 2
    elif percent >= 70:
        grade_points = 1.66
    elif percent >= 67:
        grade_points = 1.33
    elif percent >= 63:
        grade_points = 1
    elif percent >= 60:
        grade_points = .66
    return grade_points * hours


def recalculate_cumulative_gpa(user):
    cumulative_hours_passed = 0
    cumulative_gpa_hours = 0
    cumulative_gpa_points = 0
    for semester in Semester.objects.filter(user=user, is_finished=True).order_by('start_date'):
        cumulative_hours_passed += semester.hours_passed
        cumulative_gpa_hours += semester.gpa_hours
        cumulative_gpa_points += semester.final_grade_points
        if cumulative_gpa_hours != 0:
            semester.cumulative_gpa = cumulative_gpa_points / cumulative_gpa_hours
        else:
            semester.cumulative_gpa = -1.0
        semester.cumulative_gpa_hours = cumulative_gpa_hours
        semester.cumulative_hours_passed = cumulative_hours_passed
        semester.save()
    for semester in Semester.objects.filter(user=user, is_finished=False).order_by('start_date'):
        cumulative_hours_passed += semester.hours_planned
        semester.cumulative_gpa_hours = 0
        semester.cumulative_hours_passed = cumulative_hours_passed
        semester.save()


class Course(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    semester = models.ForeignKey(Semester)

    hours = models.IntegerField(default=3)

    final_grade = models.CharField(max_length=2,
                                   choices=GRADE_CHOICES,
                                   default=NONE_YET)
    final_grade_points = models.FloatField(default=0)

    not_specified_worth = models.FloatField(default=100)

    total_weighted_percentage = models.FloatField(default=0)
    total_worth_used = models.FloatField(default=0)
    course_grade = models.FloatField(default=0)

    min_weighted_percentage = models.FloatField(default=0)
    course_min_grade = models.FloatField(default=0)
    max_weighted_percentage = models.FloatField(default=0)
    course_max_grade = models.FloatField(default=0)

    course_grade_points = models.FloatField(default=0)
    course_min_grade_points = models.FloatField(default=0)
    course_max_grade_points = models.FloatField(default=0)

    def set_hours(self, hours):
        ### Remove current course from semester
        self.semester.remove_course(course=self)
        ### Change data
        self.hours = hours
        ### Add current course back to semester
        self.semester.add_course(course=self)
        ### Save current course and return
        self.save()

    def set_final_grade(self, final_grade):
        ### Remove current course from semester
        self.semester.remove_course(course=self)
        ### Change data
        self.final_grade = final_grade
        self.final_grade_points = letter_grade_to_grade_points(self.final_grade, self.hours)
        ### Add current course back to semester
        self.semester.add_course(course=self)
        ### Save current course and return
        self.save()

    ### THIS METHOD SHOULD NEVER BE CALLED WITHOUT AN ACCOMPYING add_category() AFTER IT
    ### These methods are used in pair by Assignment.set_point() and Assignment.change_category()
    ###     and Category.set_worth()
    def remove_category(self, category):
        print '4'
        ### Remove current course from semester
        self.semester.remove_course(course=self)
        ### Remove category from current course
        if category.actual_total_points != 0:
            self.total_weighted_percentage -= category.category_weighted_percentage
            self.total_worth_used -= category.worth
        self.min_weighted_percentage -= category.min_category_weighted_percentage
        self.max_weighted_percentage -= category.max_category_weighted_percentage
        self.not_specified_worth += category.worth
        ### Calculate current course's percentages and grade points
        if self.total_worth_used == 0:
            self.course_grade = 0
        else:
            self.course_grade = self.total_weighted_percentage / self.total_worth_used * 100
        if self.not_specified_worth == 100:
            self.course_min_grade = self.min_weighted_percentage
            self.course_max_grade = self.max_weighted_percentage
        else:
            self.course_min_grade = self.min_weighted_percentage / (100-self.not_specified_worth) * 100
            self.course_max_grade = self.max_weighted_percentage / (100-self.not_specified_worth) * 100
        self.course_grade_points = percentage_grade_to_grade_points(self.course_grade, self.hours)
        self.course_min_grade_points = percentage_grade_to_grade_points(self.course_min_grade, self.hours)
        self.course_max_grade_points = percentage_grade_to_grade_points(self.course_max_grade, self.hours)
        ### Save current course and return
        self.save()
        print '4.5'

    def add_category(self, category):
        print '5'
        ### Add category back to current course
        self.not_specified_worth -= category.worth
        if category.actual_total_points != 0:
            self.total_weighted_percentage += category.category_weighted_percentage
            self.total_worth_used += category.worth
        self.min_weighted_percentage += category.min_category_weighted_percentage
        self.max_weighted_percentage += category.max_category_weighted_percentage
        ### Calculate current course's percentages and grade points
        if self.total_worth_used == 0:
            self.course_grade = 0
        else:
            self.course_grade = self.total_weighted_percentage / self.total_worth_used * 100
        if self.not_specified_worth == 100:
            self.course_min_grade = self.min_weighted_percentage
            self.course_max_grade = self.max_weighted_percentage
        else:
            self.course_min_grade = self.min_weighted_percentage / (100-self.not_specified_worth) * 100
            self.course_max_grade = self.max_weighted_percentage / (100-self.not_specified_worth) * 100
        self.course_grade_points = percentage_grade_to_grade_points(self.course_grade, self.hours)
        self.course_min_grade_points = percentage_grade_to_grade_points(self.course_min_grade, self.hours)
        self.course_max_grade_points = percentage_grade_to_grade_points(self.course_max_grade, self.hours)
        ### Add current course back to semester
        self.semester.add_course(course=self)
        ### Save current course and return
        self.save()
        print '5.5'

    def __unicode__(self):
        return self.number + ' - ' + self.name


class CourseForm(forms.ModelForm):
    hours = forms.ChoiceField(choices=[(i, i) for i in range(8)])

    class Meta:
        model = Course
        fields = ['name', 'number', 'instructor', 'final_grade']
        widgets = {'name': forms.TextInput(attrs={'autocomplete': 'off'}),
                   'number': forms.TextInput(attrs={'autocomplete': 'off'}),
                   'instructor': forms.TextInput(attrs={'autocomplete': 'off'}),
                   }


class Category(models.Model):
    name = models.CharField(max_length=200)
    worth = models.FloatField()
    course = models.ForeignKey(Course)
    
    actual_points_earned = models.FloatField(default=0)
    actual_total_points = models.FloatField(default=0)
    max_points_earned = models.FloatField(default=0)
    total_points = models.FloatField(default=0)

    category_percentage = models.FloatField(default=0)
    category_weighted_percentage = models.FloatField(default=0)
    min_category_percentage = models.FloatField(default=0)
    max_category_percentage = models.FloatField(default=0)
    min_category_weighted_percentage = models.FloatField(default=0)
    max_category_weighted_percentage = models.FloatField(default=0)
    
    def set_worth(self, worth):
        ### Remove current category from course
        self.course.remove_category(category=self)
        ### Change data
        self.worth = float(worth)
        ### The next 13 lines calculate the category's percentages
        if self.actual_total_points == 0:
            self.category_percentage = 0
        else:
            self.category_percentage = self.actual_points_earned / self.actual_total_points * 100
        self.category_weighted_percentage = self.category_percentage * self.worth / 100
        if self.total_points == 0:
            self.min_category_percentage = 0
            self.max_category_percentage = 100
        else:
            self.min_category_percentage = self.actual_points_earned / self.total_points * 100
            self.max_category_percentage = self.max_points_earned / self.total_points * 100
        self.min_category_weighted_percentage = self.min_category_percentage * self.worth / 100
        self.max_category_weighted_percentage = self.max_category_percentage * self.worth / 100
        ### Add current category back to course
        self.course.add_category(category=self)
        ### Save current category and return
        self.save()

    ### THIS METHOD SHOULD NEVER BE CALLED WITHOUT AN ACCOMPYING add_assignment() AFTER IT
    ### These methods are used in pair by Assignment.set_point() and Assignment.change_category()
    def remove_assignment(self, assignment):
        print '2'
        ### Remove current category from course
        self.course.remove_category(category=self)
        ### Remove assignment from current category
        self.total_points -= assignment.total_points
        if assignment.grade_unknown:
            self.max_points_earned -= assignment.total_points
        else:
            self.actual_points_earned -= assignment.points_earned
            self.actual_total_points -= assignment.total_points
            self.max_points_earned -= assignment.points_earned
        ### The next 13 lines calculate the category's percentages
        if self.actual_total_points == 0:
            self.category_percentage = 0
        else:
            self.category_percentage = self.actual_points_earned / self.actual_total_points * 100
        self.category_weighted_percentage = self.category_percentage * self.worth / 100
        if self.total_points == 0:
            self.min_category_percentage = 0
            self.max_category_percentage = 100
        else:
            self.min_category_percentage = self.actual_points_earned / self.total_points * 100
            self.max_category_percentage = self.max_points_earned / self.total_points * 100
        self.min_category_weighted_percentage = self.min_category_percentage * self.worth / 100
        self.max_category_weighted_percentage = self.max_category_percentage * self.worth / 100
        ### Save current category and return
        self.save()
        print '2.5'

    def add_assignment(self, assignment):
        print '3'
        ### Add assignment to current category
        self.total_points += assignment.total_points
        if assignment.grade_unknown:
            self.max_points_earned += assignment.total_points
        else:
            self.actual_points_earned += assignment.points_earned
            self.actual_total_points += assignment.total_points
            self.max_points_earned += assignment.points_earned
        ### The next 13 lines calculate the category's percentages
        if self.actual_total_points == 0:
            self.category_percentage = 0
        else:
            self.category_percentage = self.actual_points_earned / self.actual_total_points * 100
        self.category_weighted_percentage = self.category_percentage * self.worth / 100
        if self.total_points == 0:
            self.min_category_percentage = 0
            self.max_category_percentage = 100
        else:
            self.min_category_percentage = self.actual_points_earned / self.total_points * 100
            self.max_category_percentage = self.max_points_earned / self.total_points * 100
        self.min_category_weighted_percentage = self.min_category_percentage * self.worth / 100
        self.max_category_weighted_percentage = self.max_category_percentage * self.worth / 100
        ### Add current category back to course
        self.course.add_category(category=self)
        ### Save current category and return
        self.save()
        print '3.5'

    def __unicode__(self):
        return self.name


class Assignment(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    
    grade_unknown = models.BooleanField(default=False)
    
    points_earned = models.FloatField(default=0)
    total_points = models.FloatField(default=0)
    percentage = models.FloatField(default=0)

    def set_points(self, grade_unknown, points_earned, total_points):
        print '1'
        ### Remove current assignment from category
        self.category.remove_assignment(assignment=self)
        ### Change data
        self.grade_unknown = grade_unknown
        self.points_earned = points_earned
        self.total_points = total_points
        ### Calculate assignment percentage
        if self.total_points == 0:
            self.percentage = 0
        else:
            self.percentage = self.points_earned / self.total_points * 100
        ### Add current assignment back to category
        self.category.add_assignment(assignment=self)
        ### Save current assignment and return
        self.save()
        print '1.5'

    def change_category(self, category):
        ### Remove current assignment from category
        self.category.remove_assignment(assignment=self)
        ### Change data
        self.category = category
        ### Add current assignment back to category
        self.category.add_assignment(assignment=self)
        ### Save current assignment and return
        self.save()

    def __unicode__(self):
        return self.name


def sanity_check_all():
    sanity_check_assignments()
    sanity_check_categories()
    sanity_check_courses()
    sanity_check_semesters()


def sanity_check_assignments():
    for assignment in Assignment.objects.all():
        if assignment.total_points == 0:
            assignment.percentage = 0
        else:
            assignment.percentage = assignment.points_earned / assignment.total_points * 100
        assignment.save()


def sanity_check_categories():
    for category in Category.objects.all():
        ### Reset category sums to zero first
        category.actual_points_earned = 0
        category.actual_total_points = 0
        category.max_points_earned = 0
        category.total_points = 0
        ### Loop through all assignments in category and add to sums appropriately
        for assignment in category.assignment_set.all():
            category.total_points += assignment.total_points
            if assignment.grade_unknown:
                category.max_points_earned += assignment.total_points
            else:
                category.actual_points_earned += assignment.points_earned
                category.actual_total_points += assignment.total_points
                category.max_points_earned += assignment.points_earned
        ### The next 13 lines calculate the category's percentages
        if category.actual_total_points == 0:
            category.category_percentage = 0
        else:
            category.category_percentage = category.actual_points_earned / category.actual_total_points * 100
        category.category_weighted_percentage = category.category_percentage * category.worth / 100
        if category.total_points == 0:
            category.min_category_percentage = 0
            category.max_category_percentage = 100
        else:
            category.min_category_percentage = category.actual_points_earned / category.total_points * 100
            category.max_category_percentage = category.max_points_earned / category.total_points * 100
        category.min_category_weighted_percentage = category.min_category_percentage * category.worth / 100
        category.max_category_weighted_percentage = category.max_category_percentage * category.worth / 100
        ### Save category and loop back to next category
        category.save()


def sanity_check_courses():
    for course in Course.objects.all():
        ### Make sure final_grade_points is correct
        course.final_grade_points = letter_grade_to_grade_points(course.final_grade, course.hours)
        ### Reset course sums to zero or 100 first
        course.not_specified_worth = 100
        course.total_weighted_percentage = 0
        course.total_worth_used = 0
        course.min_weighted_percentage = 0
        course.max_weighted_percentage = 0
        ### Loop through all categories in course and add to sums appropriately
        for category in course.category_set.all():
            course.not_specified_worth -= category.worth
            if category.actual_total_points != 0:
                course.total_weighted_percentage += category.category_weighted_percentage
                course.total_worth_used += category.worth
            course.min_weighted_percentage += category.min_category_weighted_percentage
            course.max_weighted_percentage += category.max_category_weighted_percentage
        ### Calculate course's percentages and grade points
        if course.total_worth_used == 0:
            course.course_grade = 0
        else:
            course.course_grade = course.total_weighted_percentage / course.total_worth_used * 100
        if course.not_specified_worth == 100:
            course.course_min_grade = course.min_weighted_percentage
            course.course_max_grade = course.max_weighted_percentage
        else:
            course.course_min_grade = course.min_weighted_percentage / (100-course.not_specified_worth) * 100
            course.course_max_grade = course.max_weighted_percentage / (100-course.not_specified_worth) * 100
        course.course_grade_points = percentage_grade_to_grade_points(course.course_grade, course.hours)
        course.course_min_grade_points = percentage_grade_to_grade_points(course.course_min_grade, course.hours)
        course.course_max_grade_points = percentage_grade_to_grade_points(course.course_max_grade, course.hours)
        ### Save course and loop back to next course
        course.save()


def sanity_check_semesters():
    for semester in Semester.objects.all():
        ### Recheck semester dates
        semester.recheck_dates()
        ### Reset semester sums to zero first
        semester.hours_planned = 0
        semester.hours_passed = 0
        semester.gpa_hours = 0
        semester.final_grade_points = 0
        semester.potential_min_grade_points = 0
        semester.potential_grade_points = 0
        semester.potential_max_grade_points = 0
        semester.potential_hours_counted = 0
        ### Loop through all courses in semester and add to sums appropriately
        for course in semester.course_set.all():
            semester.hours_planned += course.hours
            if course.final_grade in PASSING_GRADES:
                semester.hours_passed += course.hours
            if course.final_grade in GPA_GRADES:
                semester.gpa_hours += course.hours
            semester.final_grade_points += course.final_grade_points
            if course.final_grade != '#':
                semester.potential_min_grade_points += course.final_grade_points
                semester.potential_grade_points += course.final_grade_points
                semester.potential_max_grade_points += course.final_grade_points
                semester.potential_hours_counted += course.hours
            elif course.total_worth_used != 0:
                semester.potential_min_grade_points += course.course_min_grade_points
                semester.potential_grade_points += course.course_grade_points
                semester.potential_max_grade_points += course.course_max_grade_points
                semester.potential_hours_counted += course.hours
        ### Calculate semester's gpa's
        if semester.final_grade_points == 0:
            semester.final_gpa = 0
        else:
            semester.final_gpa = semester.final_grade_points / semester.gpa_hours
        if semester.potential_hours_counted == 0:
            semester.potential_min_gpa = 0
            semester.potential_gpa = 0
            semester.potential_max_gpa = 0
        else:
            semester.potential_min_gpa = semester.potential_min_grade_points / semester.potential_hours_counted
            semester.potential_gpa = semester.potential_grade_points / semester.potential_hours_counted
            semester.potential_max_gpa = semester.potential_max_grade_points / semester.potential_hours_counted
        ### Save semester and loop back to next semester
        semester.save()
    ### After all semester data is good, recalculate cumulative gpa
    for user in User.objects.all():
        recalculate_cumulative_gpa(user)
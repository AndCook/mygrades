from django.db import models
from decimal import Decimal
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
    gpa_points = models.FloatField(default=0)
    final_gpa = models.FloatField(default=-1.0)

    cumulative_gpa = models.FloatField(default=-1.0)
    cumulative_hours_passed = models.IntegerField(default=0)

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


def letter_grade_to_gpa_points(letter_grade, hours):
    gpa_points = 0
    if letter_grade[0] == 'A':
        gpa_points = 4
    elif letter_grade[0] == 'B':
        gpa_points = 3
    elif letter_grade[0] == 'C':
        gpa_points = 2
    elif letter_grade[0] == 'D':
        gpa_points = 1
    if len(str(letter_grade)) == 2:
        if letter_grade[1] == '+':
            gpa_points += 0.33
        elif letter_grade[1] == '-':
            gpa_points -= 0.33
        else:  # to account for CR
            gpa_points = 0
    return gpa_points * hours


class Course(models.Model):
    name = models.CharField(max_length=200)
    hours = models.IntegerField(default=3)
    number = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    semester = models.ForeignKey(Semester)

    final_grade = models.CharField(max_length=2,
                                   choices=GRADE_CHOICES,
                                   default=NONE_YET)
    gpa_points = models.FloatField(default=0)

    def __unicode__(self):
        return self.number + " - " + self.name


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

    def __unicode__(self):
        return self.course.number + " - " + self.name + " - %" + str(self.worth)


class Assignment(models.Model):
    name = models.CharField(max_length=200)
    awardedPoints = models.DecimalField(max_digits=5, decimal_places=2)
    possiblePoints = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    category = models.ForeignKey(Category)

    def save(self, *args, **kwargs):
        #calculate assignment percentage
        if self.possiblePoints == 0:
            self.percentage = 0
        else:
            self.percentage = self.awardedPoints / self.possiblePoints * Decimal(100)

        super(Assignment, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
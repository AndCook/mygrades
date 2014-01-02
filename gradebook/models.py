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


class Course(models.Model):
    name = models.CharField(max_length=200)
    hours = models.IntegerField(default=3)
    number = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    semester = models.ForeignKey(Semester)

    def __unicode__(self):
        return self.number + " - " + self.name


class CourseForm(forms.ModelForm):
    hours = forms.ChoiceField(choices=[(i, i) for i in range(8)])

    class Meta:
        model = Course
        fields = ['name', 'number', 'instructor']
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
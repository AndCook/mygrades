from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.forms import ModelForm


class Semester(models.Model):
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User, default=None)

    def __unicode__(self):
        return self.name


class SemesterForm(ModelForm):
    class Meta:
        model = Semester
        fields = ['name']


class Course(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    semester = models.ForeignKey(Semester)

    def __unicode__(self):
        return self.number + " - " + self.name


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'number', 'instructor']


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
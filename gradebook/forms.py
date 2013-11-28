from django import forms
from gradebook.models import Semester


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name']

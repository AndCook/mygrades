from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'value': 'Username',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'value': 'First Name',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'value': 'Last Name',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'value': 'Email',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))

    password1 = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'password',
               'value': 'Password',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))

    password2 = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'password',
               'value': 'Confirm Password',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
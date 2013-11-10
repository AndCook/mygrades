from collections import OrderedDict
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst


# based on LoginForm in django source code
class MyLoginForm(forms.Form):
    error_messages = {
        'invalid_login': "Invalid email/password combination",
    }

    email_field = forms.CharField(required=True,
                                  widget=forms.PasswordInput( # use instead of TextInput to remove text on load
                                      attrs={'value': 'Email',
                                             'type': 'text',
                                             'autocomplete': 'off',
                                             'onfocus': "if(this.value==this.defaultValue)this.value='';",
                                             'onblur': "if(this.value=='')this.value=this.defaultValue;"}),

                                  )

    password_field = forms.CharField(required=True,
                                     widget=forms.PasswordInput(
                                         attrs={'value': 'Password',
                                                'type': 'text',
                                                'onfocus': "if(this.value==this.defaultValue) {"
                                                           "this.value='';"
                                                           "this.type='password'; }",
                                                'onblur': "if(this.value=='') {"
                                                          "this.value=this.defaultValue;"
                                                          "this.type='text'; }"})
                                     )

    def clean(self):
        email = self.cleaned_data.get('email_field')
        password = self.cleaned_data.get('password_field')

        potential_user = authenticate(username=email, password=password)
        if potential_user is None or not potential_user.is_active:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )
        return self.cleaned_data


# based on UserCreationForm in django source code
class MyUserCreationForm(forms.Form):
    error_messages = {
        'duplicate_email': 'A user with that email already exists.',
        'all_fields_required': 'All fields are required',
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    email = forms.EmailField(widget=forms.PasswordInput(
        attrs={'value': 'Email',
               'type': 'text',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"})
    )
    first_name = forms.CharField(widget=forms.PasswordInput(
        attrs={'value': 'First Name',
               'type': 'text',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"})
    )
    last_name = forms.CharField(widget=forms.PasswordInput(
        attrs={'value': 'Last Name',
               'type': 'text',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"})
    )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'value': 'Password',
               'type': 'text',
               'onfocus': "if(this.value==this.defaultValue) {"
                          "this.value='';"
                          "this.type='password'; }",
               'onblur': "if(this.value=='') {"
                         "this.value=this.defaultValue;"
                         "this.type='text'; }"})
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'value': 'Password Confirmation',
               'type': 'text',
               'onfocus': "if(this.value==this.defaultValue) {"
                          "this.value='';"
                          "this.type='password'; }",
               'onblur': "if(this.value=='') {"
                         "this.value=this.defaultValue;"
                         "this.type='text'; }"})
    )

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        if email == '' or email == 'Email':
            raise forms.ValidationError(
                self.error_messages['all_fields_required'],
                code='all_fields_required'
            )
        try:
            User._default_manager.get(username=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 == '' or password2 == '':
            raise forms.ValidationError(
                self.error_messages['all_fields_required'],
                code='all_fields_required'
            )
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password1

    def clean(self):
        cleaned_data = super(MyUserCreationForm, self).clean()
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        if first_name == '' or first_name == 'First Name' or last_name == '' or last_name == 'Last Name':
            raise forms.ValidationError(
                self.error_messages['all_fields_required'],
                code='all_fields_required'
            )
        return cleaned_data


class MyChangeSettingsForm(forms.Form):
    error_messages = {
        'duplicate_email': 'A user with that email already exists.',
        'all_fields_required': 'All fields are required',
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    email = forms.EmailField(widget=forms.PasswordInput(
        attrs={'value': 'Email',
               'type': 'text',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"})
    )
    first_name = forms.CharField(widget=forms.PasswordInput(
        attrs={'value': 'First Name',
               'type': 'text',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"})
    )
    last_name = forms.CharField(widget=forms.PasswordInput(
        attrs={'value': 'Last Name',
               'type': 'text',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"})
    )

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        if email == '' or email == 'Email':
            raise forms.ValidationError(
                self.error_messages['all_fields_required'],
                code='all_fields_required'
            )
        try:
            User._default_manager.get(username=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean(self):
        cleaned_data = super(MyChangeSettingsForm, self).clean()
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        if first_name == '' or first_name == 'First Name' or last_name == '' or last_name == 'Last Name':
            raise forms.ValidationError(
                self.error_messages['all_fields_required'],
                code='all_fields_required'
            )
        return cleaned_data


# A combination of PasswordChangeForm and SetPasswordForm in django source code
class MyPasswordChangeForm(forms.Form):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    error_messages = {
        'password_incorrect': "Your old password was entered incorrectly. Please enter it again.",
        'password_mismatch': "The two password fields didn't match.",
    }
    old_password = forms.CharField(label="Old password",
                                   widget=forms.PasswordInput(
                                       attrs={'value': 'Old Password',
                                              'type': 'text',
                                              'onfocus': "if(this.value==this.defaultValue) {"
                                                         "this.value='';"
                                                         "this.type='password'; }",
                                              'onblur': "if(this.value=='') {"
                                                        "this.value=this.defaultValue;"
                                                        "this.type='text'; }"}),)
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput(
                                        attrs={'value': 'New Password',
                                               'type': 'text',
                                               'onfocus': "if(this.value==this.defaultValue) {"
                                                          "this.value='';"
                                                          "this.type='password'; }",
                                               'onblur': "if(this.value=='') {"
                                                         "this.value=this.defaultValue;"
                                                         "this.type='text'; }"}),)
    new_password2 = forms.CharField(label="New password confirmation",
                                    widget=forms.PasswordInput(
                                        attrs={'value': 'New Password Confirmation',
                                               'type': 'text',
                                               'onfocus': "if(this.value==this.defaultValue) {"
                                                          "this.value='';"
                                                          "this.type='password'; }",
                                               'onblur': "if(this.value=='') {"
                                                         "this.value=this.defaultValue;"
                                                         "this.type='text'; }"}),)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if self.user is None or not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

MyPasswordChangeForm.base_fields = OrderedDict(
    (k, MyPasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)
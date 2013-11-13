from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# based on LoginForm in django source code
class MyLoginForm(forms.Form):
    error_messages = {
        'invalid_login': "Invalid email/password combination",
    }

    email_field = forms.CharField(required=True,
                                  widget=forms.PasswordInput(  # use instead of TextInput to remove text on load
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
        cleaned_data = super(MyLoginForm, self).clean()

        email = cleaned_data.get('email_field')
        password = cleaned_data.get('password_field')

        potential_user = authenticate(username=email, password=password)
        if potential_user is None:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )
        return cleaned_data


# based on UserCreationForm in django source code
class MyUserCreationForm(forms.Form):
    error_messages = {
        'duplicate_email': 'A user with that email already exists.',
        'all_fields_required': 'All fields are required',
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    email = forms.CharField(widget=forms.PasswordInput(
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
        email = self.cleaned_data.get('email')
        if email == '' or email == 'Email':
            raise forms.ValidationError(
                self.error_messages['all_fields_required'],
                code='all_fields_required'
            )
        if User.objects.filter(username=email).count():
            raise forms.ValidationError(
                self.error_messages['duplicate_email'],
                code='duplicate_email',
            )
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name == 'First Name' or first_name == '':
            raise forms.ValidationError(
                self.error_messages['all_fields_required'],
                code='all_fields_required'
            )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name == 'Last Name' or last_name == '':
            raise forms.ValidationError(
                self.error_messages['all_fields_required'],
                code='all_fields_required'
            )
        return last_name


class MyChangeSettingsForm(forms.Form):
    error_messages = {
        'duplicate_email': 'A user with that email already exists.',
        'incorrect_validation': 'Incorrect validation code',
    }

    validation_code = forms.CharField(required=False,
                                      widget=forms.PasswordInput(
                                          attrs={'value': 'Validation Code',
                                                 'type': 'text',
                                                 'autocomplete': 'off',
                                                 'onfocus': "if(this.value==this.defaultValue)this.value='';",
                                                 'onblur': "if(this.value=='')this.value=this.defaultValue;"})
    )
    email = forms.CharField(required=False,
                            widget=forms.PasswordInput(
                                attrs={'value': 'Email',
                                       'type': 'text',
                                       'autocomplete': 'off',
                                       'onfocus': "if(this.value==this.defaultValue)this.value='';",
                                       'onblur': "if(this.value=='')this.value=this.defaultValue;"})
    )
    first_name = forms.CharField(required=False,
                                 widget=forms.PasswordInput(
                                     attrs={'value': 'First Name',
                                            'type': 'text',
                                            'autocomplete': 'off',
                                            'onfocus': "if(this.value==this.defaultValue)this.value='';",
                                            'onblur': "if(this.value=='')this.value=this.defaultValue;"})
    )
    last_name = forms.CharField(required=False,
                                widget=forms.PasswordInput(
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
        if User.objects.filter(username=email).count():
            raise forms.ValidationError(
                self.error_messages['duplicate_email'],
                code='duplicate_email',
            )
        return email


# A combination of PasswordChangeForm and SetPasswordForm in django source code
class MyPasswordChangeForm(forms.Form):
    error_messages = {
        'password_incorrect': 'Old password was incorrect.',
        'password_mismatch': 'The two password fields didn\'t match.',
    }
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'value': 'Old Password',
               'type': 'text',
               'onfocus': "if(this.value==this.defaultValue) {"
                          "this.value='';"
                          "this.type='password'; }",
               'onblur': "if(this.value=='') {"
                         "this.value=this.defaultValue;"
                         "this.type='text'; }"})
    )
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'value': 'New Password',
               'type': 'text',
               'onfocus': "if(this.value==this.defaultValue) {"
                          "this.value='';"
                          "this.type='password'; }",
               'onblur': "if(this.value=='') {"
                         "this.value=this.defaultValue;"
                         "this.type='text'; }"})
    )
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'value': 'New Password Confirmation',
               'type': 'text',
               'onfocus': "if(this.value==this.defaultValue) {"
                          "this.value='';"
                          "this.type='password'; }",
               'onblur': "if(this.value=='') {"
                         "this.value=this.defaultValue;"
                         "this.type='text'; }"})
    )
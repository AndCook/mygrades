from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst


class LoginForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput(
                                   attrs={'value': 'Username',
                                          'autocomplete': 'off',
                                          'onfocus': "if(this.value==this.defaultValue)this.value='';",
                                          'onblur': "if(this.value=='')this.value=this.defaultValue;"}),
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'value': 'Password',
               'type': 'text',
               'onfocus': "if(this.value==this.defaultValue) {"
                          "this.value='';"
                          "this.type='password'; }",
               'onblur': "if(this.value=='') {"
                         "this.value=this.defaultValue;"
                         "this.type='text'; }"})
    )

    error_messages = {
        'invalid_login':
        "Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserCreateForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': "A user with that username already exists.",
        'password_mismatch': "The two password fields didn't match.",
    }

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'value': 'First Name',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'value': 'Last Name',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'value': 'Email',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))
    username = forms.RegexField(label="Username", max_length=30,
                                widget=forms.TextInput(
                                    attrs={'value': 'Username',
                                           'autocomplete': 'off',
                                           'onfocus': "if(this.value==this.defaultValue)this.value='';",
                                           'onblur': "if(this.value=='')this.value=this.defaultValue;"}),
                                regex=r'^[\w.@+-]+$',
                                help_text="Required. 30 characters or fewer. Letters, digits and @.+-_ only.",
                                error_messages={
                                    'invalid': "This value may contain only letters, numbers and @.+-_ characters."}
                                )
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(
                                    attrs={'value': 'Password',
                                           'type': 'text',
                                           'onfocus': "if(this.value==this.defaultValue) {"
                                                      "this.value='';"
                                                      "this.type='password'; }",
                                           'onblur': "if(this.value=='') {"
                                                     "this.value=this.defaultValue;"
                                                     "this.type='text'; }"}),
                                )
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput(
                                    attrs={'value': 'Password Confirmation',
                                           'type': 'text',
                                           'onfocus': "if(this.value==this.defaultValue) {"
                                                      "this.value='';"
                                                      "this.type='password'; }",
                                           'onblur': "if(this.value=='') {"
                                                     "this.value=this.defaultValue;"
                                                     "this.type='text'; }"}),
                                help_text="Enter the same password as above, for verification."
                                )

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ChangeSettingsForm(forms.Form):
    error_messages = {
        'duplicate_username': "A user with that username already exists.",
    }

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'value': 'First Name',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'value': 'Last Name',
               'autocomplete': 'off',
               'onfocus': "if(this.value==this.defaultValue)this.value='';",
               'onblur': "if(this.value=='')this.value=this.defaultValue;"}
    ))

    username = forms.RegexField(label="Username", max_length=30,
                                widget=forms.TextInput(
                                    attrs={'value': 'Username',
                                           'autocomplete': 'off',
                                           'onfocus': "if(this.value==this.defaultValue)this.value='';",
                                           'onblur': "if(this.value=='')this.value=this.defaultValue;"}),
                                regex=r'^[\w.@+-]+$',
                                help_text="Required. 30 characters or fewer. Letters, digits and @.+-_ only.",
                                error_messages={
                                    'invalid': "This value may contain only letters, numbers and @.+-_ characters."}
                                )

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class UpdatePasswordForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'password_incorrect': "Your old password was entered incorrectly. "
                                "Please enter it again.",
    }

    old_password = forms.CharField(label="Old Password",
                                   widget=forms.PasswordInput(
                                       attrs={'value': 'Old Password',
                                              'type': 'text',
                                              'onfocus': "if(this.value==this.defaultValue) {"
                                                         "this.value='';"
                                                         "this.type='password'; }",
                                              'onblur': "if(this.value=='') {"
                                                        "this.value=this.defaultValue;"
                                                        "this.type='text'; }"}),
                                   help_text="Enter your current password."
                                   )

    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(
                                    attrs={'value': 'New Password',
                                           'type': 'text',
                                           'onfocus': "if(this.value==this.defaultValue) {"
                                                      "this.value='';"
                                                      "this.type='password'; }",
                                           'onblur': "if(this.value=='') {"
                                                     "this.value=this.defaultValue;"
                                                     "this.type='text'; }"}),
                                )
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput(
                                    attrs={'value': 'New Password Confirmation',
                                           'type': 'text',
                                           'onfocus': "if(this.value==this.defaultValue) {"
                                                      "this.value='';"
                                                      "this.type='password'; }",
                                           'onblur': "if(this.value=='') {"
                                                     "this.value=this.defaultValue;"
                                                     "this.type='text'; }"}),
                                help_text="Enter the same password as above, for verification."
                                )

    #class Meta:
        #model = User
        #fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def save(self, commit=True):
        user = super(UpdatePasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
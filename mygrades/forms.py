from django import forms
from django.contrib.auth.models import User


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
    username = forms.RegexField(label="Username", max_length=30,
                                widget=forms.TextInput(
                                    attrs={'value': 'Username',
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


        #attrs={'value': 'Username',
        #       'onfocus': "if(this.value==this.defaultValue)this.value='';",
        #       'onblur': "if(this.value=='')this.value=this.defaultValue;"}
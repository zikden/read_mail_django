from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class EmailDataForm(forms.Form):
    email_login = forms.CharField(label="email_login", max_length=100)
    email_password = forms.CharField(label="email_password", max_length=100)

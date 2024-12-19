"""
This module defines the forms used in the profile app.

It includes:
    - A custom registration form whith Bootstrap.
    - A restration form for creating new users.
    - A profile form for updating profiles.
"""

from profile.models import Profile

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class BootstrapAuthenticationForm(AuthenticationForm):
    """
    Authentication form with Bootstrap.
    """
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=gettext_lazy("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RegisterForm(UserCreationForm):
    """
    Form for registering a new user.
    """
    email = forms.EmailField()

    class Meta:
        """
        Meta options for RegisterForm.
        """
        User = get_user_model()
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    """
    Form for editing a profile.
    """

    class Meta:
        """
        Meta options for ProfileForm.
        """
        model = Profile
        fields = ['profile_pic', 'description']

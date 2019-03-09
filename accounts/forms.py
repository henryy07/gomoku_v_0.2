from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

from core import models

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    # Form for user registration with email, and user validation
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,
                               label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(required=True,
                                label='Repeat password',
                                widget=forms.PasswordInput,)
    first_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')

    def clean_username(self):
        # username validation
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('The field cannot be empty')
        qs = User.objects.filter(username=username)
        if qs.exists():
            print('username')
            raise ValidationError(f'{username} already exists')
        return username

    def clean_email(self):
        # email validation
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('Field cannot be empty')
        qs = User.objects.filter(email=email)
        if qs.exists():
            print('email')
            raise ValidationError(
                f'that email address {email} is already taken')
        return email

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if not password or not password2:
            raise forms.ValidationError('Both password fields cannot be empty')
        if password != password2:
            raise ValidationError('Passwords don\'t match')


class UserEditForm(forms.ModelForm):
    """Form for editing user data"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'email')

    def clean_email(self):
        """Email validation"""
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('Field cannot be empty')
        qs = User.objects.filter(email=email)
        if qs.exists():
            print('email')
            raise ValidationError(
                f'that email address {email} is already taken')

    # def clean_password(self):
    #     """Checking if password is valid for the user"""
    #     user = self.request.user or self.user
    #     password = self.cleaned_data['password']
    #     if authenticate(username=user, password=password):
    #         return password


class UserProfileEditForm(forms.ModelForm):
    """Form for editing user profile picture"""

    class Meta:
        model = models.UserProfile
        fields = ('picture',)
        widgets = {
            'picture': forms.FileInput()
        }


class UserPasswordChangeForm(forms.Form):
    current_password = forms.CharField(required=True,
                                label='Current password',
                                widget=forms.PasswordInput)
    new_password = forms.CharField (required=True,
                                label='New password',
                                widget=forms.PasswordInput)
    re_new_password = forms.CharField (required=True,
                                 label='Repeat new password',
                                 widget=forms.PasswordInput, )

    class Meta:
        model = User
        fields = ('current_password', 'new_password', 're_new_password')

    def clean_password2(self):
        password = self.cleaned_data['new_password']
        password2 = self.cleaned_data['re_new_password']
        if not password or not password2:
            raise forms.ValidationError(
                'Both password fields cannot be empty')
        if password != password2:
            raise ValidationError('Passwords don\'t match')

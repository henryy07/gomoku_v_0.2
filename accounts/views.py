from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth import get_user_model

from . import forms
from core import models

User = get_user_model()


class RegisterView(View):
    """Class that handles registration process"""

    def get(self, request):
        """function handling GET method"""
        form = forms.UserRegisterForm()
        return render(
            request,
            'registration/registration_form.html',
            {'form': form})

    def post(self, request):
        """function handling POST method"""
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/home')

        ctx = {
            'form': form
        }
        return render(request, 'registration/registration_form.html', ctx)


class UserProfileView(LoginRequiredMixin, DetailView):
    """Detail view of user profile"""
    queryset = models.UserProfile.objects.all()
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        """adding user form, userprofile form and user context to the view"""
        ctx = super(UserProfileView, self).get_context_data(**kwargs)
        ctx['user_form'] = forms.UserEditForm()
        ctx['userprofile_form'] = forms.UserProfileEditForm()
        ctx['user'] = self.request.user
        return ctx

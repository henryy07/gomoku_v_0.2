"""Urls for basic views"""
from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("help/", views.HelpView.as_view(), name="help"),
]

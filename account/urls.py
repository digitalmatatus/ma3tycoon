"""URL's for the account app."""

from django.urls import path

from . import views

urlpatterns = [
    path('settings/', views.Settings.as_view()),
    path('password/', views.Password.as_view()),
]
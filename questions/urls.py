"""URL's for the questions app."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.QuestionsView.as_view()),
]
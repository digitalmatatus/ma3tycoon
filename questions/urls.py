"""URL's for the questions app."""

from django.urls import path

from . import views

urlpatterns = [
    path('trivia/', views.TriviaQuestionsView.as_view()),
    path('transit/', views.TransitQuestionsView.as_view()),
]
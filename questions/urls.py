"""URL's for the questions app."""

from django.urls import path

from . import views

urlpatterns = [
    path('trivia/', views.TriviaQuestions.as_view()),
    path('transit/', views.TransitQuestions.as_view()),
    path('leaderboard/', views.LeaderBoard.as_view()),
    path('analysis/', views.Analysis.as_view()),
]
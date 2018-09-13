"""URL's for the fares app."""

from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.AddFareView.as_view()),
    path('budget/', views.BudgetFareView.as_view()),
]
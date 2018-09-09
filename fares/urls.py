"""URL's for the fares app."""

from django.urls import path

from . import views

urlpatterns = [
    path('budget/', views.BudgetView.as_view()),
]
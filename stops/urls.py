"""URL's for the stops app."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.StopsView.as_view()),
]

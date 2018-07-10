"""URL's for the routes app."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.RoutesView.as_view()),
]

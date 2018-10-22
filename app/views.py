"""Views for the basic app."""

from django.http import Http404
from django.shortcuts import render


def raise_404():
    """Raise a 404 Error."""
    raise Http404


def index(request):
    return render(request, 'app/index.html')

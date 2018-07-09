"""Views for the basic app."""

from django.http import Http404


def raise_404():
    """Raise a 404 Error."""
    raise Http404

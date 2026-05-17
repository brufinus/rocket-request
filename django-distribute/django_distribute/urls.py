"""URL patterns for the Distribute app."""

# pylint: disable=invalid-name

from django.urls import path

from . import views

app_name = "distribute"
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("results/", views.results, name="results"),
    path("api/collection/", views.item_collection, name="collection"),
    path("api/distributable/", views.distributable, name="distributable"),
    path("api/remove/", views.remove, name="remove"),
    path("api/reset/", views.reset, name="reset"),
]

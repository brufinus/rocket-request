from django.urls import path

from . import views

app_name = "distribute"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/collection/", views.item_collection, name="collection"),
    path("api/remove/", views.remove, name="remove"),
    path("api/distributable/", views.distributable, name="distributable"),
    path("results/", views.results, name="results"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
]

from django.urls import path

from . import views

app_name = "distribute"
urlpatterns = [
    path("", views.index, name="index"),
    path("collection/", views.item_collection, name="collection"),
    path("results/", views.results, name="results"),
]

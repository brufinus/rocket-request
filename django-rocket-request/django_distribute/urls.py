from django.urls import path

from . import views

app_name = "distribute"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/collection/", views.item_collection, name="collection"),
    path("api/remove/", views.remove, name="remove"),
    path("api/distribute/", views.distribute, name="distribute"),
    path("results/", views.results, name="results"),
]

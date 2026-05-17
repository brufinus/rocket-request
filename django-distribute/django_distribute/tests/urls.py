from django.urls import path, include

app_name = "distribute"
urlpatterns = [
    path("distribute/", include("django_distribute.urls", namespace="distribute"))
]

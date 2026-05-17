"""Distribute app configuration."""

from django.apps import AppConfig


class DistributeConfig(AppConfig):
    """Defines configuration for the distribute app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_distribute"
    label = "distribute"

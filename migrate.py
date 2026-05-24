#!/usr/bin/env python
"""Makes migration files then migrates them."""

from django.core.management import call_command
from boot_django import boot_django

boot_django()
call_command("makemigrations", "distribute")
call_command("migrate")

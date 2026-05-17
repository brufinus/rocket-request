=================
django-rocket-request
=================

django-rocket-request is a Django app that shows you how to
distribute a set of items amongst rocket silos in Factorio.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "distribute" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_distribute",
    ]

2. Include the distribute URLconf in your project urls.py like this::

    path("distribute/", include("django_distribute.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server.

5. Visit the ``/distribute/`` URL to start using the app.
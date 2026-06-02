"""
Views for the distribute app.

Functions:
    index: Renders the main page of the application.
    item_collection: API that updates the itemlist.
    remove: API that removes an item from the itemlist.
    distributable: API that validates the session for distribution.
    results: Renders the Results page with distributed data.
    contact: Renders the Contact page.
    about: Renders the About page.
    reset: API that resets the itemlist.
    import_blueprint: API that imports items from a blueprint string.
"""

import logging

from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django_distribute.data.constants import Errors
from django_distribute.data.items import ITEMS
from django_distribute.exceptions import (
    ChestIndexException,
    InvalidBlueprintException,
    InvalidItemException,
)
from django_distribute.services.blueprint import (
    convert_blueprint,
    extract_items_from_json,
)
from django_distribute.services.distribution import distribute_items
from django_distribute.services.initialize_setup import (
    build_consolidated_blueprint,
    build_consolidated_invs,
    build_consolidated_load,
    build_distribution,
    group_items,
)
from django_distribute.services.search import search_coordinator
from django_distribute.services.validation import is_max_count

logger = logging.getLogger(__name__)


def index(request):
    """
    Renders the main page of the application.

    The current itemlist and potential on-load
    errors are passed to the template.
    """
    itemlist = request.session.get("itemlist", {})
    request.session["itemlist"] = dict(sorted(itemlist.items()))

    table_headers = ("Item", "Count")
    if not itemlist:
        table_headers = (Errors.NO_ITEMS_ADDED, "")

    distribute_error = request.session.pop("distribute_error", "")
    if distribute_error:
        logger.warning("Distribute error triggered: %s", distribute_error)
    import_error = request.session.pop("import_error", "")
    if import_error:
        logger.warning("Import error triggered: %s", import_error)

    return render(
        request,
        "distribute/index.html",
        {
            "distribute_error": distribute_error,
            "import_error": import_error,
            "itemlist": request.session["itemlist"],
            "suggestions": ITEMS,
            "table_headers": table_headers,
        },
    )


def item_collection(request):
    """
    Updates the itemlist.

    Only adds valid or similar matches to the given item name.
    The item count is incremented if it already exists in the list.
    """
    if request.method == "POST":
        # Item validation
        item = request.POST.get("user-item")
        search_res = search_coordinator(item, ITEMS)
        if search_res[0]:
            item_name = search_res[0]
        else:
            logger.warning("User attempted to add an invalid item: %s", item)
            return JsonResponse({"itemlist": "Invalid item"})

        try:
            item_count: int = int(request.POST.get("user-count"))
        except ValueError:
            logger.warning(
                "User input an invalid count: %s", request.POST.get("user-count")
            )
            return JsonResponse({"itemlist": "Invalid count"})
        if int(item_count) <= 0:
            logger.warning("User input an invalid count: %s", item_count)
            return JsonResponse({"itemlist": "Invalid count"})

        total_count = request.session.get("c", 0) + item_count
        if is_max_count(total_count):
            logger.warning("User hit the max item count limit")
            return JsonResponse({"itemlist": "Max count"})
        request.session["c"] = total_count
        itemlist: dict[str, int] = request.session.get("itemlist", {})
        if item_name in itemlist:
            item_count += int(itemlist[item_name])
        itemlist.update({item_name: item_count})
        request.session["itemlist"] = dict(sorted(itemlist.items()))
        logger.info("%s added, total count: %s", item_name, total_count)
        return JsonResponse({"itemlist": request.session["itemlist"]})
    logger.error("User submitted an invalid request: %s", request.method)
    return HttpResponseBadRequest()


def remove(request):
    """Removes an item from the itemlist."""
    if request.method == "POST":
        item_name = request.POST.get("user-item")
        itemlist: dict[str, int] = request.session.get("itemlist", {})
        if item_name in itemlist:
            total_count = request.session.get("c", 0) - itemlist[item_name]
            request.session["c"] = total_count
            del itemlist[item_name]
            logger.info("%s removed, total count: %s", item_name, total_count)
        request.session["itemlist"] = itemlist
        return JsonResponse({"itemlist": request.session["itemlist"]})
    logger.error("User submitted an invalid request: %s", request.method)
    return HttpResponseBadRequest()


def distributable(request):
    """
    Checks whether the session is valid for distribution.

    The session is valid when the itemlist has at least one item and
    the user has entered a valid number of silos.
    """
    itemlist: dict = request.session.get("itemlist", {})
    if not itemlist:
        request.session["distribute_error"] = Errors.ADD_ITEMS_DISTRIBUTE
        return HttpResponseRedirect(reverse("distribute:index"))
    try:
        num_silos = request.POST["num-silos"]
    except KeyError:
        logger.error("User attempted to distribute without num_silos")
        return HttpResponseBadRequest()
    request.session["num_silos"] = num_silos
    return HttpResponseRedirect(reverse("distribute:results"))


def results(request):
    """
    Renders the Results page with the distributed data.

    Consolidated data is built and passed to the results template, which
    iterates over and displays the data in a consumable way.
    """
    num_silos = 0
    try:
        num_silos: int = int(request.session.get("num_silos", -1))
    except ValueError:
        logger.warning(
            "Session contains invalid num_silos: %s", request.session.get("num_silos")
        )
        return HttpResponseRedirect(reverse("distribute:index"))
    if num_silos <= 0 or num_silos > 100:
        logger.warning("Session num_silos is out of bounds: %s", num_silos)
        return HttpResponseRedirect(reverse("distribute:index"))

    itemlist: dict[str, int] = request.session.get("itemlist", None)
    if itemlist is None or not itemlist:
        logger.warning("Session is missing the itemlist")
        return HttpResponseRedirect(reverse("distribute:index"))

    silos = distribute_items(itemlist)
    cycles = build_distribution(silos, num_silos, ITEMS)

    c_silo_invs = build_consolidated_invs(silos, num_silos, ITEMS)
    c_silo_loads = build_consolidated_load(silos, num_silos)
    consolidated = zip(c_silo_invs, c_silo_loads)

    try:
        blueprint = build_consolidated_blueprint(c_silo_invs)
    except ChestIndexException:
        logger.warning("At least one consolidated blueprint exceeds available slots")
        blueprint = Errors.ITEMS_EXCEED_SLOTS

    count = request.session.get("c", "0")
    logger.info(
        "%s items distributed amongst %s silos, rendering results", count, num_silos
    )
    return render(
        request,
        "distribute/results.html",
        {
            "num_silos": num_silos,
            "num_launches": len(silos),
            "num_cycles": len(cycles),
            "cycles": cycles,
            "consolidated": consolidated,
            "blueprint": blueprint,
        },
    )


def contact(request):
    """Renders the Contact page."""
    return render(request, "distribute/contact.html")


def about(request):
    """Renders the About page."""
    return render(request, "distribute/about.html")


def reset(request):
    """Resets the itemlist and redirects back to index."""
    request.session["itemlist"] = {}
    request.session["c"] = 0
    logger.info("Session has been reset")
    return HttpResponseRedirect(reverse("distribute:index"))


def import_blueprint(request):
    """
    Imports items to the itemlist from a given blueprint string.

    Items are extracted from the blueprint string and added to the
    itemlist. The index page is rendered with errors set in the session
    if the process fails.
    """
    if request.method == "POST":
        blueprint = request.POST.get("blueprint-input")
        if blueprint and len(blueprint) < 50000:
            try:
                json_rep = convert_blueprint(blueprint)
            except InvalidBlueprintException:
                request.session["import_error"] = Errors.IMPORT_ERROR
                return HttpResponseRedirect(reverse("distribute:index"))
            try:
                items = extract_items_from_json(json_rep, ITEMS)
            except InvalidItemException as e:
                request.session["import_error"] = f"{Errors.INVALID_ITEM}{e.item}"
                return HttpResponseRedirect(reverse("distribute:index"))

            total_count = len(items)
            if is_max_count(total_count):
                request.session["import_error"] = Errors.BP_ITEMS_EXCEED_MAX
                return HttpResponseRedirect(reverse("distribute:index"))
            request.session["c"] = total_count
            itemlist = group_items(items, ITEMS)
            request.session["itemlist"] = dict(sorted(itemlist.items()))
            logger.info("Blueprint successfully imported. Total count: %s", total_count)
        return HttpResponseRedirect(reverse("distribute:index"))
    logger.error("User submitted an invalid request: %s", request.method)
    return HttpResponseBadRequest()

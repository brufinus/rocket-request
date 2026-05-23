"""Views for the distribute app."""

from importlib.metadata import version as get_version

from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django_distribute.data.constants import Errors
from django_distribute.data.items import ITEMS
from django_distribute.exceptions import InvalidBlueprintException, InvalidItemException
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

table_item_count = ("Item", "Count")


def index(request):
    """Main page for the application."""
    itemlist = request.session.get("itemlist", {})
    request.session["itemlist"] = dict(sorted(itemlist.items()))
    table_headers = table_item_count
    if not itemlist:
        table_headers = (Errors.NO_ITEMS_ADDED, "")

    distribute_error = request.session.pop("distribute_error", "")
    import_error = request.session.pop("import_error", "")

    return render(
        request,
        "distribute/index.html",
        {
            "distribute_error": distribute_error,
            "import_error": import_error,
            "itemlist": request.session["itemlist"],
            "suggestions": ITEMS,
            "table_headers": table_headers,
            "version": get_version("django-distribute"),
        },
    )


def item_collection(request):
    """
    Updates the item list by updating or adding items to it.

    Only adds valid or similar matches for item name.
    Updates the item count if it already exists in the list.
    """
    if request.method == "POST":
        # Item validation
        search_res = search_coordinator(request.POST.get("user-item"), ITEMS)
        if search_res[0]:
            item_name = search_res[0]
        else:
            return JsonResponse({"itemlist": "Invalid item"})

        item_count: int = int(request.POST.get("user-count"))
        if int(item_count) <= 0:
            return JsonResponse({"itemlist": "Invalid count"})

        itemlist: dict[str, int] = request.session.get("itemlist", {})
        if item_name in itemlist:
            item_count += int(itemlist[item_name])
        itemlist.update({item_name: item_count})
        request.session["itemlist"] = dict(sorted(itemlist.items()))
        return JsonResponse({"itemlist": request.session["itemlist"]})
    return HttpResponseBadRequest()


def remove(request):
    """Removes an item from the item list."""
    if request.method == "POST":
        item_name = request.POST.get("user-item")
        itemlist: dict[str, int] = request.session.get("itemlist", {})
        if item_name in itemlist:
            del itemlist[item_name]
        request.session["itemlist"] = itemlist
        return JsonResponse({"itemlist": request.session["itemlist"]})
    return HttpResponseBadRequest()


def distributable(request):
    """Checks whether the session is valid for distribution."""
    itemlist: dict = request.session.get("itemlist", {})
    if len(itemlist) <= 0:
        request.session["distribute_error"] = Errors.ADD_ITEMS_DISTRIBUTE
        return HttpResponseRedirect(reverse("distribute:index"))
    try:
        num_silos = request.POST["num-silos"]
    except KeyError:
        return HttpResponseBadRequest()
    request.session["num_silos"] = num_silos
    return HttpResponseRedirect(reverse("distribute:results"))


def results(request):
    """Renders the results page with the distributed data."""
    # Pop session keys if wanting to reset values after distribution.
    num_silos: int = int(request.session.get("num_silos", -1))
    if num_silos <= 0:
        return HttpResponseRedirect(reverse("distribute:index"))

    itemlist: dict[str, int] = request.session.get("itemlist", None)
    if itemlist is None or not itemlist:
        return HttpResponseRedirect(reverse("distribute:index"))
    silos = distribute_items(itemlist)
    cycles = build_distribution(silos, num_silos, ITEMS)

    c_silo_invs = build_consolidated_invs(silos, num_silos, ITEMS)
    c_silo_loads = build_consolidated_load(silos, num_silos)
    consolidated = zip(c_silo_invs, c_silo_loads)

    return render(
        request,
        "distribute/results.html",
        {
            "num_silos": num_silos,
            "num_launches": len(silos),
            "num_cycles": len(cycles),
            "cycles": cycles,
            "consolidated": consolidated,
            "version": get_version("django-distribute"),
            "blueprint": build_consolidated_blueprint(c_silo_invs),
        },
    )


def contact(request):
    """Renders the Contact page."""
    return render(
        request,
        "distribute/contact.html",
        {"version": get_version("django-distribute")},
    )


def about(request):
    """Renders the About page."""
    return render(
        request, "distribute/about.html", {"version": get_version("django-distribute")}
    )


def reset(request):
    """Resets the itemlist and redirects back to index."""
    request.session["itemlist"] = {}
    return HttpResponseRedirect(reverse("distribute:index"))


def import_blueprint(request):
    """Imports items from a given blueprint string."""
    if request.method == "POST":
        blueprint = request.POST.get("blueprint-input")
        if blueprint:
            try:
                json_rep = convert_blueprint(blueprint)
            except InvalidBlueprintException:
                request.session["import_error"] = Errors.IMPORT_ERROR
                return HttpResponseRedirect(reverse("distribute:index"))
            try:
                items = extract_items_from_json(json_rep, ITEMS)
            except InvalidItemException as e:
                request.session["import_error"] = (
                    f"{Errors.INVALID_ITEM}{e.item}"
                )
                return HttpResponseRedirect(reverse("distribute:index"))
            itemlist = request.session.get("itemlist", {})
            itemlist = group_items(items, ITEMS)
            request.session["itemlist"] = dict(sorted(itemlist.items()))
        return HttpResponseRedirect(reverse("distribute:index"))
    return HttpResponseBadRequest()

"""Views for the distribute app."""

from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django_distribute.data.items import ITEMS
from django_distribute.services.distribution import distribute_items
from django_distribute.services.initialize_setup import (
    build_consolidated_invs,
    build_consolidated_load,
    build_distribution,
)
from django_distribute.services.search import search_coordinator


def index(request):
    """Main page for the application."""
    request.session.set_test_cookie()

    itemlist = request.session.get("itemlist", {})
    request.session["itemlist"] = dict(sorted(itemlist.items()))

    distribute_error = request.session.pop("distribute_error", None)

    return render(
        request,
        "distribute/index.html",
        {
            "itemlist": request.session["itemlist"],
            "suggestions": ITEMS,
            "distribute_error": distribute_error,
        },
    )


def item_collection(request):
    """
    Updates the item list by updating or adding items to it.

    Only adds valid or similar matches for item name.
    Updates the item count if it already exists in the list.
    """
    if request.method == "POST":
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            print("Cookie test!")
        else:
            # TODO: Handle missing cookie
            print("Please enable cookies and try again.")

        # Item validation
        search_res = search_coordinator(request.POST.get("user-item"), ITEMS)
        # TODO: Confirmation on similar result.
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
        request.session["distribute_error"] = "Please add items to distribute."
        return HttpResponseRedirect(reverse("distribute:index"))
    try:
        num_silos = request.POST["num_silos"]
    except KeyError:
        return HttpResponseBadRequest()
    request.session["num_silos"] = num_silos
    return HttpResponseRedirect(reverse("distribute:results"))


def results(request):
    """Renders the results page with the distributed data."""
    # Pop session keys if wanting to reset values after distribution.
    num_silos: int = int(request.session.get("num_silos", None))
    if num_silos is None:
        return HttpResponseRedirect(reverse("distribute:index"))

    silos = distribute_items(request.session.get("itemlist", None))
    if silos is None:
        return HttpResponseRedirect(reverse("distribute:index"))
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
        },
    )

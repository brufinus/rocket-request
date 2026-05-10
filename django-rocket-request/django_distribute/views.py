from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django_distribute.data.items import ITEMS
from django_distribute.services.search import search_coordinator


def index(request):
    """Main page for the application."""
    request.session.set_test_cookie()

    items = request.session.get("items", [])
    request.session["items"] = items
    item_names = []
    item_counts = []
    for item in items:
        item_names.append(item[0])
        item_counts.append(item[1])

    return render(
        request,
        "distribute/index.html",
        {"items": item_names, "counts": item_counts, "suggestions": ITEMS},
    )


def item_collection(request):
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
            return JsonResponse({"items": "Invalid item"})

        item_count = request.POST.get("user-count")
        if item_count <= 0:
            return JsonResponse({"items": "Invalid count"})

        items = request.session.get("items", [])
        items.append((item_name, item_count))
        request.session["items"] = items
        return JsonResponse({"items": items})
    return HttpResponseBadRequest()


def results(request):
    try:
        num_silos = request.POST["num_silos"]
    except KeyError:
        return render(request, "distribute/index.html", None)
    else:
        return render(
            request,
            "distribute/results.html",
            {"num_silos": num_silos, "num_launches": 6, "num_cycles": 2},
        )

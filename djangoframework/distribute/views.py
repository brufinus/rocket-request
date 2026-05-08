from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render


def index(request):
    return render(request, "distribute/index.html", None)


def results(request):
    try:
        num_silos = request.POST["num_silos"]
    except KeyError:
        return render(request, "distribute/index.html", None)
    else:
        return render(request, "distribute/results.html", {"num_silos": num_silos})

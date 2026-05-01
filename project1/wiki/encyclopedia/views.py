import markdown 
from django.shortcuts import render
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    encyc_list = util.list_entries()
    if not encyc_list or name not in encyc_list:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.markdown(util.get_entry(name)),
            "name": name
        })
    
def search(request):
    query = request.GET.get("q", "")
    encyc_list = util.list_entries()
    if query in encyc_list:
        return HttpResponseRedirect(reverse("wiki:entry", args=[query]))
    else:
        results = [entry for entry in encyc_list if query.lower() in entry.lower()]
        if not results:
            return render(request, "encyclopedia/error.html", {
                "message": "No entries found."
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "entries": results,
                "name": query
            })
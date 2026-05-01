from django.shortcuts import render
import markdown 
from . import util


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
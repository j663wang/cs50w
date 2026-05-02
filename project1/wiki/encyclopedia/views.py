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
        
def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:entry", args=[title]))
    else:
        return render(request, "encyclopedia/create.html")
    
def edit(request, name):
    if request.method == "POST":
        content = request.POST.get("content", "")
        util.save_entry(name, content)
        return HttpResponseRedirect(reverse("wiki:entry", args=[name]))
    else:
        entry_content = util.get_entry(name)
        if entry_content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry not found."
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "name": name,
                "content": entry_content
            })
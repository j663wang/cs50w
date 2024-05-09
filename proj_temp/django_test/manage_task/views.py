from django.shortcuts import render

taskLst= ["a","b","c"]
# Create your views here.
def index(request):
    return render(request, "manage_task/index.html",{
        "taskLst": taskLst
    })
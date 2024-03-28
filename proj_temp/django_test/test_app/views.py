from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("This is test app")

def helloWorld(request):
    return HttpResponse("Hello world")

def greet(request, name):
    return HttpResponse(f"Hi {name}")

def test(request, input):
    return render(request,"test/test.html",{
        "var": input
    })
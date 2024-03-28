from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    #path("<str:name>",views.greet, name="greet"),
    path("<str:input>",views.test, name="test"),
    path("helloWorld", views.helloWorld, name="helloWorld")
] 
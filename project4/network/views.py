from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import *


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    if posts.count() == 0:
        return JsonResponse({
        "posts": [],
        "total_pages": 0,
        "current_page": 0
    })
    else:
        posts = Post.objects.all().order_by('-timestamp')
        paginator = Paginator(posts, 10)  # 10 posts per page
        page_num = request.GET.get('page', 1)
        page = paginator.get_page(page_num)
        return JsonResponse({
        "posts": [{"content": p.content, "user": p.user.username} for p in page],
        "total_pages": paginator.num_pages,
        "current_page": page.number
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def newPost(request):
    if request.method == "POST":
        content = request.POST["postContent"]
        post = Post(user=request.user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/newPost.html")
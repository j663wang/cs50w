import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm

from accounts.models import User
from decks.models import Deck

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email',  'password'] 

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["comfirm_pass"]
        if password != confirmation:
            return render(request, "accounts/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "accounts/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("social:"))
    else:
        return render(request, "accounts/register.html")
    
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("social:index"))
        else:
            return render(request, "accounts/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("defaultpage:index"))

@login_required
def profile_view(request, username):
    user = User.objects.filter(username=username).first()
    if not user:
        return HttpResponse("User not found", status=404)
    followers_num = user.followers.count()
    following_num = user.following.count()
    is_following = True if user.followers.filter(id=request.user.id).exists() else False

    return JsonResponse({
        "profile_username": user.username,
        "email": user.email,
        "followers": followers_num,
        "following": following_num,
        "is_following": is_following,
        "short_bio": user.bio[:50] + "..." if len(user.bio) > 50 else user.bio,
    })
    

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:profile', kwargs={'username': request.user.username}))
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/update.html', {'form': form})
            
                
                
            
            
            
        

from django.urls import path

from . import views

urlpatterns = [
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("follow/<str:username>", views.follow_toggle, name="follow_toggle"),
]

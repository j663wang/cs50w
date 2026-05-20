
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("edit/<int:post_id>", views.editPost, name="editPost"),
    path("likePost/<int:post_id>", views.likePost, name="likePost"),
    path("post/<int:post_id>", views.getPost, name="getPost"),
    path("creator/<int:post_id>", views.isCreator, name="isCreator")
]

from django.urls import path

from . import views

urlpatterns = [
    path("follow/<str:username>", views.follow_toggle, name="follow_toggle"),
    path("like/deck/<int:deck_id>", views.like_toggle_deck, name="like_toggle_deck"),
    path("like/card/<int:card_id>", views.like_toggle_card, name="like_toggle_card"),
]

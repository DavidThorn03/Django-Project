from django.urls import path

from . import views

app_name = "holidays"
urlpatterns = [
    path("", views.index, name="index"),
    path("hotel/<int:hotel_id>/", views.hotel, name="hotel"),
    path("profile/<int:client_id>/", views.profile, name="profile"),
    path("book/<int:hotel_id>/", views.book, name="book"),
]
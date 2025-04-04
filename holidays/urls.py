from django.urls import path

from . import views

app_name = "holidays"
urlpatterns = [
    path("", views.index, name="index"),
    path("hotel/<int:hotel_id>/", views.hotel, name="hotel"),
    path("profile/", views.profile, name="profile"),
    path("book/<int:room_id>/", views.book, name="book"),
    path("make_booking/", views.make_booking, name="make_booking"),
    path("cancel_booking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("login/", views.login, name="login"),
    path("login_user/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("register/", views.register, name="register"),
    path("register_user/", views.register_user, name="register_user"),
]
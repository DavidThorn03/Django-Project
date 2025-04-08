from django.urls import path

from . import views

app_name = "holidays"
urlpatterns = [
    # client pages
    path("", views.index, name="index"),
    path("hotel/<int:hotel_id>/", views.hotel, name="hotel"),
    path("profile/", views.profile, name="profile"),
    path("book/<int:room_id>/", views.book, name="book"),
    path("cancel_booking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("rate/<int:hotel_id>/<int:rating>/", views.rate, name="rate"),

    #staff pages
    path("staff_index/", views.staff_index, name="staff_index"),
    path("staff_room/<int:room_id>/", views.staff_room, name="staff_room"),

    # authentication pages
    path("login/", views.login, name="login"),
    path("logout/", views.logout_user, name="logout_user"),
    path("register/", views.register, name="register"),
]
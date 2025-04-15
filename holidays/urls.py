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
    path("pay_booking/<int:booking_id>/", views.pay_booking, name="pay_booking"),
    path("contact/<int:hotel_id>/", views.contact, name="contact"),

    #staff pages
    path("staff_index/", views.staff_index, name="staff_index"),
    path("staff_room/<int:room_id>/", views.staff_room, name="staff_room"),
    path("approve_booking/<int:booking_id>/", views.approve_booking, name="approve_booking"),
    path("remove_booking/<int:booking_id>/", views.remove_booking, name="remove_booking"),
    path("view_client/<int:client_id>/", views.view_client, name="view_client"),
    path("feedback/<int:query_id>/", views.feedback, name="feedback"),

    #admin pages
    path("admin_index/", views.admin_index, name="admin_index"),
    path("edit_hotel/", views.edit_hotel, name="edit_hotel"),
    path("edit_room/<int:room_id>/", views.edit_room, name="edit_room"),
    path("add_room/", views.add_room, name="add_room"),
    path("delete_room/<int:room_id>/", views.delete_room, name="delete_room"),
    path("add_admin/", views.add_admin, name="add_admin"),
    path("add_staff/", views.add_staff, name="add_staff"),

    # authentication pages
    path("login/", views.login, name="login"),
    path("logout/", views.logout_user, name="logout_user"),
    path("register/", views.register, name="register"),
]
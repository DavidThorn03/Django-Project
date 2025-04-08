from django.contrib import admin

# Register your models here.
from .models import Hotel, Room, User, Client, WebAdmin, Staff, Booking, Rating, Query, Feedback

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(User)
admin.site.register(Client)
admin.site.register(WebAdmin)
admin.site.register(Staff)
admin.site.register(Booking)
admin.site.register(Rating)
admin.site.register(Query)
admin.site.register(Feedback)
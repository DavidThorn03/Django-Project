from django.contrib import admin

# Register your models here.
from .models import Hotel, Room, User, Client, WebAdmin, Staff, Booking

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(User)
admin.site.register(Client)
admin.site.register(WebAdmin)
admin.site.register(Staff)
admin.site.register(Booking)
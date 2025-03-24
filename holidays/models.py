from django.db import models


#Hotel models

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact = models.IntegerField(default=0)
    email = models.CharField(max_length=200)
    #rating = models.IntegerField(default=0)
    def __str__(self):
        return self.hotel_name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    number = models.IntegerField(default=0)
    def __str__(self):
        return self.description


#User models

class User(models.Model):
    user_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    def __str__(self):
        return self.user_name

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    address = models.CharField(max_length=200)
    def __str__(self):
        return self.user.user_name

class WebAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    privilege = models.IntegerField(default=0)
    def __str__(self):
        return self.user.user_name

class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.user_name


#Hotel user models

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField("check in date")
    check_out = models.DateTimeField("check out date")
    def __str__(self):
        return self.user.user_name + " " + self.room.description

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    def __str__(self):
        return self.user.user_name + " " + self.hotel.hotel_name + " " + str(self.rating)

"""
Change your models (in models.py).

Run python manage.py makemigrations to create migrations for those changes

Run python manage.py migrate to apply those changes to the database



from holidays.models import Hotel, Room, User, Client, WebAdmin, Staff, Booking, Rating
"""
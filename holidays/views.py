from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from datetime import datetime

from .models import Hotel, Client, Room, Booking, User, WebAdmin, Staff, Rating

# Client pages


def index(request):
    hotels = Hotel.objects.all()
    user = request.COOKIES.get("user_name")
    print(user)
    context = {'hotels': hotels, "user": user}
    return render(request, 'holidays/index.html', context)

def hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    return render(request, 'holidays/hotel.html', {'hotel': hotel})

def profile(request):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    try:
        user = get_object_or_404(Client, user=user)
    except Http404:
        return redirect("holidays:login")
        
    return render(request, 'holidays/profile.html', {'client': user})


def book(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    user = request.COOKIES.get("user_id")
    
    if request.method == "POST":
        check_in = request.POST["check_in"]
        check_out = request.POST["check_out"]

        try:
            check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            return Http404("Invalid date format.")

        if not is_Client(user):
            return redirect("holidays:login")
        
        new = Booking(user_id=user, room_id=room_id, check_in=check_in, check_out=check_out)

        if not new.valid_dates():
            return Http404("Check-in date must be before check-out date.")
        
        new.save()
        return redirect("holidays:profile")  
        
    if is_Client(user):
        return render(request, 'holidays/book.html', {'room': room, 'user_id': user})
    
    return redirect("holidays:login")

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    elif int(user) == booking.user_id:
        booking.delete()
        return redirect("holidays:profile")
    
    return redirect("holidays:index")


def rate(request, hotel_id, rating):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    user = request.COOKIES.get("user_id")
    if not is_Client(user):
        return redirect("holidays:login")
        
    try:
        Rating.objects.update_or_create(
            hotel_id = hotel.id,
            user_id = user,
            defaults = {'rating': int(rating)}
        )
        return redirect("holidays:hotel", hotel_id=hotel_id)
    except Exception as e:
        return redirect("holidays:index")
    


# staff pages


def staff_index(request): 
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        staff = get_object_or_404(Staff, user_id=user)
    except Http404:
        return redirect("holidays:login")
        
    hotel = get_object_or_404(Hotel, id=staff.hotel_id)
    
    return render(request, 'holidays/staff_index.html', {"hotel": hotel})


def staff_room(request, room_id):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        staff = get_object_or_404(Staff, user_id=user)
    except Http404:
        return redirect("holidays:login")
        
    hotel = get_object_or_404(Hotel, id=staff.hotel_id)
    
    room = get_object_or_404(Room, id=room_id)

    if room.hotel_id != hotel.id:
        return redirect("holidays:staff_index")

    bookings = room.unapproved_bookings()
    
    
    return render(request, 'holidays/staff_room.html', {"room": room, "bookings": bookings})



# authentication pages

def login(request):
    if request.method == "POST":
        username = request.POST["user_name"]
        password = request.POST["password"]
        try:
            user = User.objects.get(user_name=username, password=password)
                
            response = redirect("holidays:index")

            if is_Staff(user.id):
                response = redirect("holidays:staff_index")
            #elif is_WebAdmin(user.id):
                #response = redirect("holidays:webadmin_index")

            response.set_cookie('user_name', user.user_name, max_age=3600)  
            response.set_cookie('user_id', user.id, max_age=3600)

            return response

        except User.DoesNotExist:
            return render(request, 'holidays/login.html')
    
    return render(request, 'holidays/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["user_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        mobile = request.POST["mobile"]
        age = request.POST["age"]
        address = request.POST["address"]
        
        try:
            if User.objects.filter(email=email).exists():
                raise Exception("Username already exists.")
            user = User.objects.create(user_name=username, email=email, password=password, mobile=mobile)
            user.save()
            client = Client.objects.create(user=user, age=age, address=address)
            client.save()
            return redirect("holidays:login")
        except Exception as e:
            return render(request, 'holidays/register.html')
        
    return render(request, 'holidays/register.html')

def logout_user(request):
    response = redirect("holidays:index")
    response.delete_cookie('user_name')
    response.delete_cookie('user_id')
    response.delete_cookie('user_type')
    return redirect("holidays:login")

def is_Client(user_id):
    try:
        user = Client.objects.get(user_id=user_id)
        return True
    except Client.DoesNotExist:
        return False
    
def is_WebAdmin(user_id):
    try:
        user = WebAdmin.objects.get(user_id=user_id)
        return True
    except WebAdmin.DoesNotExist:
        return False
    
def is_Staff(user_id):
    try:
        user = Staff.objects.get(user_id=user_id)
        return True
    except Staff.DoesNotExist:
        return False
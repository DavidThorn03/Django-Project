from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from datetime import datetime

from .models import Hotel, Client, Room, Booking, User, WebAdmin, Staff, Rating, Query, Feedback

# Client pages


def index(request):
    hotels = Hotel.objects.all()
    user = request.COOKIES.get("user_name")
    context = {'hotels': hotels, "user": user}
    return render(request, 'holidays/index.html', context)

def hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    user = request.COOKIES.get("user_name")
    context = {'hotel': hotel, "user": user}
    return render(request, 'holidays/hotel.html', context)

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
        
        user = get_object_or_404(Client, user=user)
        
        new = Booking(user_id=user.id, room_id=room_id, check_in=check_in, check_out=check_out)

        if not new.valid_dates():
            return render(request, 'holidays/book.html', {'room': room})
        
        new.save()
        return redirect("holidays:profile")  
        
    if is_Client(user):
        return render(request, 'holidays/book.html', {'room': room})
    
    return redirect("holidays:login")

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    user = request.COOKIES.get("user_id")
    if not is_Client(user):
        return redirect("holidays:login")
    
    user = get_object_or_404(Client, user=user)

    if user.id == booking.user_id:
        booking.delete()
        return redirect("holidays:profile")
    
    return redirect("holidays:index")


def rate(request, hotel_id, rating):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    user = request.COOKIES.get("user_id")
    try:
        user = get_object_or_404(Client, user=user)
    except Http404:
        return redirect("holidays:login")
        
    try:
        Rating.objects.update_or_create(
            hotel_id = hotel.id,
            user_id = user.id,
            defaults = {'rating': int(rating)}
        )
        return redirect("holidays:hotel", hotel_id=hotel_id)
    except Exception as e:
        return redirect("holidays:index")
    
def pay_booking(request, booking_id):
    user = request.COOKIES.get("user_id")
    if not is_Client(user):
        return redirect("holidays:login")
    
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if request.method == "POST":
        # propcess user info here if payment system is used 
        if request.POST["card_number"] == "":
            return render(request, 'holidays/pay_booking.html', {'booking': booking})
        booking.payed = True
        booking.save()
        return redirect("holidays:profile")
    
    else: 
        return render(request, 'holidays/pay_booking.html', {'booking': booking})
    

def contact(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    user = request.COOKIES.get("user_id")
    if not is_Client(user):
        return redirect("holidays:login")
    try:
        user = get_object_or_404(Client, user=user)
    except Http404:
        return redirect("holidays:login")
        
    if request.method == "POST":
        subject = request.POST["subject"]
        query = request.POST["query"]
        new = Query(user_id=user.id, hotel_id=hotel_id, subject=subject, query=query, date=datetime.now(), status=False)
        new.save()
        return redirect("holidays:hotel", hotel_id=hotel_id)
    
    return render(request, 'holidays/contact.html', {'hotel': hotel})
    


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


def approve_booking(request, booking_id):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        staff = get_object_or_404(Staff, user_id=user)
    except Http404:
        return redirect("holidays:login")
        
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.room.hotel_id != staff.hotel_id:
        return redirect("holidays:staff_index")

    booking.approved = staff
    booking.save()
    
    return redirect("holidays:staff_room", room_id=booking.room.id)


def remove_booking(request, booking_id):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        staff = get_object_or_404(Staff, user_id=user)
    except Http404:
        return redirect("holidays:login")
        
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.room.hotel_id != staff.hotel_id:
        return redirect("holidays:staff_index")

    booking.delete()
    
    return redirect("holidays:staff_room", room_id=booking.room.id)


def view_client(request, client_id):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        staff = get_object_or_404(Staff, user_id=user)
    except Http404:
        return redirect("holidays:login")
        
    client = get_object_or_404(Client, id=client_id)
    
    bookings = Booking.objects.filter(user=client, room__hotel_id=staff.hotel_id)

    
    return render(request, 'holidays/view_client.html', {"client": client, "bookings": bookings})

def feedback(request, query_id):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        staff = get_object_or_404(Staff, user_id=user)
    except Http404:
        return redirect("holidays:login")
        
    query = get_object_or_404(Query, id=query_id)
    
    if query.hotel_id != staff.hotel_id:
        return redirect("holidays:login")

    if request.method == "POST":
        feedback = request.POST["feedback"]
        new = Feedback(query_id=query.id, feedback=feedback, staff=staff, date=datetime.now())
        new.send_feedback()
        return redirect("holidays:staff_index")
    
    return render(request, 'holidays/feedback.html', {"query": query})



# WebAdmin pages
def admin_index(request):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        webadmin = get_object_or_404(WebAdmin, user_id=user)
    except Http404:
        return redirect("holidays:login")
        
    hotel = get_object_or_404(Hotel, id=webadmin.hotel_id)
    
    return render(request, 'holidays/admin_index.html', {"hotel": hotel, "admin": webadmin})


def edit_hotel(request):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        webadmin = get_object_or_404(WebAdmin, user_id=user)
    except Http404:
        return redirect("holidays:login")
    
    if webadmin.privilege > 0:
        return redirect("holidays:login")
        
    hotel = get_object_or_404(Hotel, id=webadmin.hotel_id)
    
    if request.method == "POST":
        hotel.description = request.POST["description"]
        hotel.location = request.POST["location"]
        hotel.address = request.POST["address"]
        hotel.email = request.POST["email"]
        hotel.contact = request.POST["contact"]
        if request.FILES.get("image") is not None:
            hotel.image = request.FILES.get("image")
            
        hotel.save()
        
        return redirect("holidays:admin_index")
    
    return render(request, 'holidays/edit_hotel.html', {"hotel": hotel})

def edit_room(request, room_id):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        webadmin = get_object_or_404(WebAdmin, user_id=user)
    except Http404:
        return redirect("holidays:login")
    
    if webadmin.privilege > 2:
        return redirect("holidays:login")
        
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == "POST":
        room.description = request.POST["description"]
        room.price = request.POST["price"]
        room.number = request.POST["num"]
        if request.FILES.get("image") is not None:
            room.image = request.FILES.get("image")

        room.save()
        
        return redirect("holidays:admin_index")
    
    return render(request, 'holidays/edit_room.html', {"room": room})


def add_room(request):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        webadmin = get_object_or_404(WebAdmin, user_id=user)
    except Http404:
        return redirect("holidays:login")
    
    if webadmin.privilege > 1:
        return redirect("holidays:login")
        
    hotel = get_object_or_404(Hotel, id=webadmin.hotel_id)
    
    if request.method == "POST":
        if Room.objects.filter(description=request.POST["description"]).exists():
            raise Exception("Room already exists.")
        
        room = Room(
            hotel=hotel,
            description=request.POST["description"],
            price=request.POST["price"],
            number=request.POST["num"],
        )
        if request.FILES.get("image") is not None:
            room.image = request.FILES.get("image")
        room.save()
        
        return redirect("holidays:admin_index")
    
    return render(request, 'holidays/add_room.html', {"hotel": hotel})


def delete_room(request, room_id):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        webadmin = get_object_or_404(WebAdmin, user_id=user)
    except Http404:
        return redirect("holidays:login")
    
    if webadmin.privilege > 1:
        return redirect("holidays:login")
        
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    
    return redirect("holidays:admin_index")

def add_admin(request):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        webadmin = get_object_or_404(WebAdmin, user_id=user)
    except Http404:
        return redirect("holidays:login")
    
    if webadmin.privilege > 0:
        return redirect("holidays:login")
        
    hotel = get_object_or_404(Hotel, id=webadmin.hotel_id)
    
    if request.method == "POST":
        username = request.POST["user_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        mobile = request.POST["mobile"]
        privilege = request.POST["privilege"]
        
        try:
            if User.objects.filter(email=email).exists():
                raise Exception("Username already exists.")
            user = User.objects.create(user_name=username, email=email, password=password, mobile=mobile)
            user.save()
            webadmin = WebAdmin.objects.create(user=user, hotel=hotel, privilege=privilege)
            webadmin.save()
            return redirect("holidays:admin_index")
        except Exception as e:
            return render(request, 'holidays/add_admin.html')
        
    return render(request, 'holidays/add_admin.html')

def add_staff(request):
    user = request.COOKIES.get("user_id")
    if user is None:
        return redirect("holidays:login")
    
    try:
        webadmin = get_object_or_404(WebAdmin, user_id=user)
    except Http404:
        return redirect("holidays:login")
    
    if webadmin.privilege > 0:
        return redirect("holidays:login")
        
    hotel = get_object_or_404(Hotel, id=webadmin.hotel_id)
    
    if request.method == "POST":
        username = request.POST["user_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        mobile = request.POST["mobile"]
        
        try:
            if User.objects.filter(email=email).exists():
                raise Exception("Username already exists.")
            user = User.objects.create(user_name=username, email=email, password=password, mobile=mobile)
            user.save()
            webadmin = Staff.objects.create(user=user, hotel=hotel)
            webadmin.save()
            return redirect("holidays:admin_index")
        except Exception as e:
            return render(request, 'holidays/add_staff.html')
        
    return render(request, 'holidays/add_staff.html')





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
            elif is_WebAdmin(user.id):
                response = redirect("holidays:admin_index")

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
    return response

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
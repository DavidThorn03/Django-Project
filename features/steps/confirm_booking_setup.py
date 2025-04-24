from behave import given, when, then
from django.urls import reverse
from holidays.models import User, Client, Hotel, Room, Booking, Staff

@given("staff is viewing booking")
def step_open_booking_page(context):
    # Create a hotel and a room for the test
    hotel = Hotel.objects.create(hotel_name="Test Hotel", location="Test Location")
    room = Room.objects.create(hotel=hotel, description="Test Room", price=100.0)
    
    # Create a user and a client for the test
    user = User.objects.create(user_name="testuser", email="test@test.com", password="testpass123", mobile=1234567890)
    client = Client.objects.create(user=user, age=25, address="123 Test Street")

    booking = Booking.objects.create(user=client, room=room, check_in="2026-10-01", check_out="2026-10-05")
    booking2 = Booking.objects.create(user=client, room=room, check_in="2026-10-02", check_out="2026-10-05")
    context.response = context.test.client.get(reverse("holidays:staff_room", kwargs={"room_id": room.id}))

@given("is logged in as staff")
def step_user_logged_in(context):
    # Create a staff user and log them in
    user = User.objects.create(user_name="staffuser", email="staff@gmail.com", password="staffpass123", mobile=9876543210)
    staff = Staff.objects.create(user=user, hotel=Hotel.objects.get(hotel_name="Test Hotel"))
    context.test.client.cookies['user_id'] = str(user.id)

@when("staff selects to approve booking")
def step_select_approve_booking(context):
    # Simulate the action of approving a booking
    booking = Booking.objects.get(check_in="2026-10-01")
    context.response = context.test.client.post(reverse("holidays:approve_booking", kwargs={"booking_id": booking.id}))

@when("staff selects to deny booking")
def step_select_deny_booking(context):
    # Simulate the action of denying a booking
    booking = Booking.objects.get(check_in="2026-10-02")
    context.response = context.test.client.post(reverse("holidays:remove_booking", kwargs={"booking_id": booking.id}))

@when("not logged in")
def step_user_not_logged_in(context):
    context.test.client.cookies.clear()

@then("the booking should be approved")
def step_check_booking_approved(context):
    # Check if the booking was approved
    booking = Booking.objects.get(check_in="2026-10-01")
    assert booking.approved is not None

@then("the booking should be removed")
def step_check_booking_removed(context):
    # Check if the booking was removed
    booking = Booking.objects.filter(check_in="2026-10-02").first()
    assert booking is None

@then("the staff should be informed")
def step_check_in_room(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:staff_room", kwargs={"room_id": Room.objects.get(description="Test Room").id})

@then("staff should be redirected to login")
def step_check_redirect_to_login(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:login")
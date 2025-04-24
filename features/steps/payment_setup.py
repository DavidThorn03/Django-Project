from behave import given, when, then
from django.urls import reverse
from holidays.models import User, Client, Hotel, Room, Booking, Staff

@given("user is in pay page")
def step_open_pay_page(context):
    # Create a hotel and room for the test
    hotel = Hotel.objects.create(hotel_name="Test Hotel", description="test", address="123 Test St", location="Test Location", contact=1234567890, email="test@hotel.com")
    room = Room.objects.create(id=1 , hotel=hotel, price=100, description="Test Room", number=101)
    # Create a user and client for the test
    user = User.objects.create(user_name="testuser", email="test@user.com", password="testpass123", mobile=1234567890)
    staff_user = User.objects.create(user_name="staffuser", email="test@staff.com", password="staffpass123", mobile=1234567890)
    staff = Staff.objects.create(user=staff_user, hotel=hotel)
    client = Client.objects.create(user=user, age=25, address="123 Test Street")
    # Create a booking for the test
    booking = Booking.objects.create(id=1, user=client, room=room, check_in="2023-10-01", check_out="2023-10-05", approved=staff, payed=False)

@given("is logged in as client")
def step_user_logged_in(context):
    user = User.objects.get(user_name="testuser")
    context.test.client.cookies['user_id'] = str(user.id)
    context.response = context.test.client.get(reverse("holidays:pay_booking", kwargs={"booking_id": Booking.objects.first().id}))

@given("the user isnt logged in as client")
def step_user_not_logged_in(context):
    context.test.client.cookies.clear()

@when("user enters correct card information")
def step_enter_valid_card_info(context):
    context.form_data = {
        "card_number": "1234567812345678",
        "expiry_date": "12/25",
        "cvv": "123",
        "cardholder_name": "Test User",
    }

@when("user enters incorrect card information")
def step_enter_invalid_card_info(context):
    context.form_data = {
        "card_number": "",
        "expiry_date": "12/20",
        "cvv": "123",
        "cardholder_name": "Test User",
    }

@when("selects pay")
def step_click_pay(context):
    context.response = context.test.client.post(reverse("holidays:pay_booking", kwargs={"booking_id": Booking.objects.first().id}), data=context.form_data)

@then("booking should be set as paid")
def step_check_success(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:profile")
    # Check if the booking was marked as paid
    booking = Booking.objects.get(id=1)
    assert booking.payed is True

@then("user should be told")
def step_check_error_message(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:profile")

@then("the user should be informed that card information is invalid")
def step_check_error_message(context):
    assert context.response.status_code == 200
    assert "pay_booking" in context.response.templates[0].name

@then("the user should be redirected to login page")
def step_check_login_redirect(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:login")
from behave import given, when, then
from django.urls import reverse
from holidays.models import User, Client, Hotel, Room, Booking
from datetime import date, timedelta

@given("user has selected room")
def step_open_register_page(context):
    # Create a hotel and room for the test
    hotel = Hotel.objects.create(hotel_name="Test Hotel", description="test", address="123 Test St", location="Test Location", contact=1234567890, email="test@test.com")
    room = Room.objects.create(id=1 , hotel=hotel, price=100, description="Test Room", number=101)
    # Create a user and client for the test
    user = User.objects.create(user_name="testuser", email="test@gmail.com", password="testpass123", mobile=1234567890)
    client = Client.objects.create(user=user, age=25, address="123 Test Street")

    context.test.client.cookies['user_id'] = str(user.id) 
    context.response = context.test.client.get(reverse("holidays:book", kwargs={"room_id": 1}))

@when("client enters check in and check out date")
def step_enter_valid_data(context):
    context.form_data = {
        "check_in": (date.today() + timedelta(8)).strftime("%Y-%m-%d"),
        "check_out": (date.today() + timedelta(10)).strftime("%Y-%m-%d"),
    }

@when("client enters invalid check in and check out date")
def step_enter_invalid_data(context):
    context.form_data = {
        "check_in": (date.today() + timedelta(2)).strftime("%Y-%m-%d"),
        "check_out": (date.today() + timedelta(1)).strftime("%Y-%m-%d"),
    }


@when("is logged in")
def step_user_logged_in(context):
    user = User.objects.get(user_name="testuser")
    context.test.client.cookies['user_id'] = str(user.id) 
    context.response = context.test.client.get(reverse("holidays:book", kwargs={"room_id": 1}))

@when("selects book")
def step_click_book(context):
    context.response = context.test.client.post(reverse("holidays:book", kwargs={"room_id": 1}), data=context.form_data)

@when("the user is not logged in")
def step_user_not_logged_in(context):
    context.test.client.cookies.clear()

@then("booking should be made and user should be brought to profile page")
def step_check_success(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:profile")
    # Check if the booking was created
    user = User.objects.get(user_name="testuser")
    client = Client.objects.get(user=user)
    room = Room.objects.get(description="Test Room")
    booking = Booking.objects.filter(user=client, room=room).first()
    assert booking is not None

@then("the user should be informed that the dates are invalid")
def step_check_error_message(context):
    assert context.response.status_code == 200
    assert "book" in context.response.templates[0].name

@then("user should be redirected to login")
def step_check_login_redirect(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:login")

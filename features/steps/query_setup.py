from behave import given, when, then
from django.urls import reverse
from holidays.models import User, Client, Hotel, Query
from datetime import datetime


@given("the user is in the contact page")
def step_user_logged_in(context):
    # Create a hotel and room for the test
    hotel = Hotel.objects.create(id=1, hotel_name="Test Hotel", description="test", address="123 Test St", location="Test Location", contact=1234567890, email="test@hotel.com")
    user = User.objects.create(user_name="user", email="user@user.com", password="pass123", mobile=1234567890)
    client = Client.objects.create(user=user, age=25, address="123 User St")
    context.test.client.cookies['user_id'] = str(user.id)
    context.response = context.test.client.get(reverse("holidays:contact", kwargs={"hotel_id": hotel.id}))

@given("isn’t logged in as client")
def step_user_not_logged_in(context):
    context.test.client.cookies.clear()

@when("the user enters their query")
def step_enter_feedback_info(context):
    context.form_data = {
        "subject": "Test Subject",
        "query": "This is a test query.",
    }

@when("selects submit query")
def step_click_submit(context):
    context.response = context.test.client.post(reverse("holidays:contact", kwargs={"hotel_id": 1}), data=context.form_data)

@then("the query should be made")
def step_check_success(context):
    user = User.objects.get(user_name="user")
    client = Client.objects.get(user=user)
    hotel = Hotel.objects.get(id=1)
    query = Query.objects.filter(user=client, hotel=hotel).first()
    assert query is not None

@then("the user should be informed")
def step_check_error_message(context):
    assert context.response.url == reverse("holidays:hotel", kwargs={"hotel_id": 1})

@then("the user should be redirected to login")
def step_check_redirect(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:login")

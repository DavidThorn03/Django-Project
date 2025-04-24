from behave import given, when, then
from django.urls import reverse
from holidays.models import User, Client

@given("the user is in the register page")
def step_open_register_page(context):
    context.response = context.test.client.get(reverse("holidays:register"))

@when("the user enters valid data and an email that isn’t in use")
def step_enter_valid_data(context):
    context.form_data = {
        "user_name": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "mobile": 1234567890,
        "age": 25,
        "address": "123 Test Street"
    }

@when("the user enters valid data and an email that is already liked to an account")
def step_enter_duplicate_email(context):
    User.objects.create(user_name="existinguser", email="test@example.com", password="abc", mobile="0000000000")
    context.form_data = {
        "user_name": "newuser",
        "email": "test@example.com",  
        "password": "newpass123",
        "mobile": 987654321,
        "age": 30,
        "address": "456 Another Street"
    }

@when("the user enters invalid data")
def step_enter_invalid_data(context):
    context.form_data = {
        "user_name": "",
        "email": "",
        "password": "short",
        "mobile": "",
        "age": "",
        "address": ""
    }

@when("the user clicks on the register button")
def step_submit_form(context):
    context.response = context.test.client.post(reverse("holidays:register"), data=context.form_data)

@then("the Client should be registered and directed to the login page")
def step_check_success(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:login")

@then("the user should be informed that an account with this email already exists")
@then("the user should be informed that the data is invalid")
def step_check_error_message(context):
    assert context.response.status_code == 200
    assert "register" in context.response.templates[0].name

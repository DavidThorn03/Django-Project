from behave import given, when, then
from django.urls import reverse
from holidays.models import User, Client

@given("the user is in the login page")
def step_open_register_page(context):
    context.response = context.test.client.get(reverse("holidays:login"))

@when("the user enters a valid email and password")
def step_enter_valid_data(context):
    User.objects.create(user_name="testuser", email="test@test.com", password="testpass123", mobile=1234567890)
    Client.objects.create(user=User.objects.get(user_name="testuser"), age=25, address="123 Test Street")
    context.form_data = {
        "user_name": "testuser",
        "password": "testpass123",
    }

@when("the user enters a email and password that do not match")
def step_enter_mismatched_data(context):
    context.form_data = {
        "user_name": "testuser",
        "password": "wrongpass",
    }

@when("the user enters a email and password that aren’t in the system")
def step_enter_nonexistent_data(context):
    context.form_data = {
        "user_name": "nonexistentuser",
        "password": "wrongpass",
    }

@when("clicks login")
def step_click_login(context):
    context.response = context.test.client.post(reverse("holidays:login"), data=context.form_data)


@then("the user should be redirected to the home page")
def step_check_success(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:index")

@then("the user should be told their email and password are incorrect")
@then("the user should be told the user doesn’t exist")
def step_check_error_message(context):
    assert context.response.status_code == 200
    assert "login" in context.response.templates[0].name
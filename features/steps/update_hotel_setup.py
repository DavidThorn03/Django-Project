from behave import given, when, then
from django.urls import reverse
from holidays.models import User, WebAdmin, Hotel

@given("the user is logged in as web admin")
def step_user_logged_in(context):
    # Create a user and web admin for the test
    user = User.objects.create(user_name="testuser", email="admin@test.com", password="testpass123", mobile=1234567890)
    hotel = Hotel.objects.create(hotel_name="Test Hotel", description="test", address="123 Test St", location="Test Location", contact=1234567890, email="hotel@test.com")
    web_admin = WebAdmin.objects.create(user=user, hotel=hotel, privilege=0)
    context.test.client.cookies['user_id'] = str(user.id)

@given("does not have permission to update hotel info")
def step_no_permission(context):
    web_admin = WebAdmin.objects.get(user__user_name="testuser")
    web_admin.privilege = 1
    web_admin.save()

@given("is on hotel page")
def step_on_hotel_page(context):
    context.response = context.test.client.get(reverse("holidays:admin_index"))

@when("the user selects the field they want to change")
def step_select_field(context):
    context.response = context.test.client.get(reverse("holidays:edit_hotel"))

@when("enters the change")
def step_enter_change(context):
    context.form_data = {
        "description": "Updated description",
        "address": "Updated address",
        "location": "Updated location",
        "contact": 9876543210,
        "email": "new@email.com",
    }

@when("selects save")
def step_click_save(context):
    context.response = context.test.client.post(reverse("holidays:edit_hotel"), data=context.form_data)

@then("the change should be saved the user should be informed")
def step_check_success(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:admin_index")
    # Check if the hotel information was updated
    hotel = Hotel.objects.get(hotel_name="Test Hotel")
    assert hotel.description == "Updated description"
    assert hotel.address == "Updated address"
    assert hotel.location == "Updated location"
    assert hotel.contact == 9876543210
    assert hotel.email == "new@email.com"

@then("the user should be directed to the login page")
def step_check_login_page(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:login")
from behave import given, when, then
from django.urls import reverse
from holidays.models import User, Client, Hotel, Room, Booking, Staff, Query, Feedback
from datetime import datetime

@given("a user is logged in as staff")
def step_user_logged_in(context):
    # Create a hotel and room for the test
    hotel = Hotel.objects.create(hotel_name="Test Hotel", description="test", address="123 Test St", location="Test Location", contact=1234567890, email="test@hotel.com")
    user = User.objects.create(user_name="staffuser", email="staff@user.com", password="staffpass123", mobile=1234567890)
    staff_user = Staff.objects.create(user=user, hotel=hotel)
    context.test.client.cookies['user_id'] = str(user.id)

@given("with the wrong hotel")
def step_user_wrong_hotel(context):
    # Create a hotel and room for the test
    hotel = Hotel.objects.create(hotel_name="Test Hotel2", description="test", address="123 Test St", location="Test Location", contact=1234567890, email="test@hotel.com")
    staff = Staff.objects.get(user__user_name="staffuser")
    staff.hotel = hotel
    staff.save()

@given("is in the query page")
def step_open_query_page(context):
    # Create a hotel and room for the test
    hotel = Hotel.objects.get(hotel_name="Test Hotel")
    user = User.objects.create(user_name="user", email="user@user.com", password="pass123", mobile=1234567890)
    client = Client.objects.create(user=user, age=25, address="123 Test Street")
    query = Query.objects.create(id=1, user=client, hotel=hotel, subject="Test", query="Test query", date=datetime.now(), status=False)
    context.response = context.test.client.get(reverse("holidays:feedback", kwargs={"query_id": query.id}))

@when("the user enters the feedback info")
def step_enter_feedback_info(context):
    context.form_data = {
        "feedback": "This is a test feedback",
    }

@when("selects submit")
def step_click_submit(context):
    context.response = context.test.client.post(reverse("holidays:feedback", kwargs={"query_id": 1}), data=context.form_data)

@then("the feedback should be saved and sent as an email to the user")
def step_check_feedback_saved(context):
    feedback = Feedback.objects.filter(query__id=1).first()
    assert feedback is not None
    assert feedback.query.status == True 
    assert feedback.feedback == context.form_data["feedback"]

@then("the staff should be informed of success")
def step_check_staff_informed(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:staff_index")

@then("the staff member should be informed that this query has already been responded to")
def step_check_responded_to(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:staff_index")

@then("the user should be redirected to the login page")
def step_check_redirect(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:login")
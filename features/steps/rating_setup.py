from behave import given, when, then
from django.urls import reverse
from holidays.models import User, Client, Hotel, Rating

@given("the user is logged in as client")
def step_user_logged_in(context):
    # Create a hotel for the test
    user = User.objects.create(user_name="testuser", email="user@user.com", password="testpass123", mobile=1234567890)
    client = Client.objects.create(user=user, age=25, address="123 Test Street")
    context.test.client.cookies['user_id'] = str(user.id) #

@given("the user is not logged in")
def step_user_not_logged_in(context):
    context.test.client.cookies.clear()

@given("is on the hotel page")
def step_on_hotel_page(context):
    # Create a hotel for the test
    hotel = Hotel.objects.create(id=1, hotel_name="Test Hotel", description="test", address="123 Test St", location="Test Location", contact=1234567890, email="test:hotel.com")
    context.response = context.test.client.get(reverse("holidays:hotel", kwargs={"hotel_id": hotel.id}))

@given("has already rated the hotel")
def step_already_rated_hotel(context):
    hotel = Hotel.objects.get(hotel_name="Test Hotel")
    client = Client.objects.get(user__user_name="testuser")
    rating = Rating.objects.create(hotel=hotel, user=client, rating=4)

@when("the user selects the rating they want to give")
def step_select_rating(context):
    context.rating = 5
    context.response = context.test.client.post(reverse("holidays:rate", kwargs={"hotel_id": 1, "rating": context.rating}))

@then("the rating should be saved")
def step_check_rating_saved(context):
    hotel = Hotel.objects.get(hotel_name="Test Hotel")
    client = Client.objects.get(user__user_name="testuser")
    rating = Rating.objects.filter(hotel=hotel, user=client).first()
    assert rating is not None
    assert rating.rating == context.rating

@then("their rating of that hotel should be updated")
def step_check_rating_updated(context):
    hotel = Hotel.objects.get(hotel_name="Test Hotel")
    client = Client.objects.get(user__user_name="testuser")
    rating = Rating.objects.filter(hotel=hotel, user=client).first()
    assert rating is not None
    assert rating.rating == 5

@then("the user should be informed of the rating")
def step_check_user_informed(context):
    assert context.response.status_code == 302
    assert context.response.url == reverse("holidays:hotel", kwargs={"hotel_id": 1})

@then("they are redirected to the login page")
def step_redirected_to_login(context):
    assert context.response.url == reverse("holidays:login")
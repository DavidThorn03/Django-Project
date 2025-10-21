from django.test import TestCase
from holidays.models import Hotel, Client, Room, Booking, User, WebAdmin, Staff, Rating, Query, Feedback
from datetime import date, timedelta, datetime

# Create your tests here.

# Rating tests

class RatingTestCase(TestCase):
    def setUp(self):
        user1 = User(user_name="user1", email="user1@test.com", password="password", mobile=1234567890)
        user1.save()
        client1 = Client(user=user1, age=20, address="Test Address")
        client1.save()
        user2 = User(user_name="user2", email="user2@test.com", password="password", mobile=1234567890)
        user2.save()
        client2 = Client(user=user2, age=20, address="Test Address")
        client2.save()
        user3 = User(user_name="user3", email="user3@test.com", password="password", mobile=1234567890)
        user3.save()
        client3 = Client(user=user3, age=20, address="Test Address")
        client3.save()

        hotel1 = Hotel(hotel_name="Test Hotel", location="Test Location", contact=22, email="test@test.com")
        hotel1.save()
        Rating.objects.create(hotel=hotel1, user=client1, rating=5)
        Rating.objects.create(hotel=hotel1, user=client2, rating=3)
        Rating.objects.create(hotel=hotel1, user=client3, rating=2)

        hotel2 = Hotel(hotel_name="Test Hotel1", location="Test Location1", contact=22, email="test1@test.com")
        hotel2.save()
        Rating.objects.create(hotel=hotel2, user=client1, rating=4)

        Hotel.objects.create(hotel_name="Test Hotel2", location="Test Location2", contact=22, email="test2@test.com")
    
    def test_get_rating(self):
        hotel = Hotel.objects.get(hotel_name="Test Hotel")
        self.assertEqual(hotel.get_rating(), 3.3)
        hotel1 = Hotel.objects.get(hotel_name="Test Hotel1")
        self.assertEqual(hotel1.get_rating(), 4.0)
        hotel2 = Hotel.objects.get(hotel_name="Test Hotel2")
        self.assertEqual(hotel2.get_rating(), 0.0)


class BookingTestCase(TestCase):
    def setUp(self):
        hotel1 = Hotel(hotel_name="Test Hotel", location="Test Location", contact=22, email="test@test.com")
        hotel1.save()
        hotel2 = Hotel(hotel_name="Test Hote2", location="Test Location", contact=22, email="test@test.com")
        hotel2.save()

        room1 = Room(hotel=hotel1, price=100, description="Test Room", number=101)
        room1.save()
        room2 = Room(hotel=hotel1, price=200, description="Test Room2", number=102)
        room2.save()
        room3 = Room(hotel=hotel2, price=300, description="Test Room3", number=103)
        room3.save()
        room4 = Room(hotel=hotel2, price=400, description="Test Room4", number=104)
        room4.save()

        user1 = User(user_name="user1", email="user1@test.com", password="password", mobile=1234567890)
        user1.save()
        client1 = Client(user=user1, age=20, address="Test Address")
        client1.save()
        user2 = User(user_name="user2", email="user2@test.com", password="password", mobile=1234567890)
        user2.save()
        client2 = Client(user=user2, age=20, address="Test Address")
        client2.save()
        user3 = User(user_name="user3", email="user3@test.com", password="password", mobile=1234567890)
        user3.save()
        client3 = Client(user=user3, age=20, address="Test Address")
        client3.save()
        user4 = User(user_name="staff1", email="staff1@test.com", password="password", mobile=1234567890)
        user4.save()
        staff1 = Staff(user=user4, hotel=hotel1)
        staff1.save()


        Booking.objects.create(user=client1, room=room1, check_in=date.today() + timedelta(1), check_out=date.today() + timedelta(5))
        Booking.objects.create(user=client1, room=room2, check_in=date.today() + timedelta(4), check_out=date.today() + timedelta(6))
        Booking.objects.create(user=client2, room=room1, check_in=date.today() + timedelta(3), check_out=date.today() + timedelta(7))
        Booking.objects.create(user=client2, room=room3, check_in=date.today() + timedelta(7), check_out=date.today() + timedelta(8))
        Booking.objects.create(user=client3, room=room2, check_in=date.today() + timedelta(2), check_out=date.today() + timedelta(9))
        Booking.objects.create(user=client3, room=room3, check_in=date.today() + timedelta(1), check_out=date.today() + timedelta(10))

        Booking.objects.create(user=client1, room=room1, check_in=date.today() + timedelta(1), check_out=date.today() + timedelta(10), approved=staff1)
        Booking.objects.create(user=client1, room=room2, check_in=date.today() + timedelta(4), check_out=date.today() + timedelta(6), approved=staff1)
        Booking.objects.create(user=client2, room=room1, check_in=date.today() + timedelta(3), check_out=date.today() + timedelta(7), approved=staff1)
        Booking.objects.create(user=client2, room=room3, check_in=date.today() + timedelta(7), check_out=date.today() + timedelta(8), approved=staff1)

    def test_get_bookings(self):
        #GET all bookings and users
        user1 = User.objects.get(user_name="user1")
        user1 = Client.objects.get(user=user1)

        room1 = Room.objects.get(description="Test Room")
        room2 = Room.objects.get(description="Test Room2")
        room3 = Room.objects.get(description="Test Room3")
        room4 = Room.objects.get(description="Test Room4")

        # test unapproved bookings
        self.assertEqual(room1.num_unapproved(), 2)
        self.assertEqual(room2.num_unapproved(), 2)
        self.assertEqual(room3.num_unapproved(), 2)
        self.assertEqual(room4.num_unapproved(), 0)

        self.assertEqual(room1.unapproved_bookings().count(), 2)
        self.assertEqual(room4.unapproved_bookings().count(), 0)

        # test valid dates
        booking2 = Booking(user=user1, room=room2, check_in=date.today() + timedelta(8), check_out=date.today() + timedelta(6))
        self.assertEqual(booking2.valid_dates(), False)
        booking3 = Booking(user=user1, room=room2, check_in=date.today() + timedelta(-2), check_out=date.today() + timedelta(6))
        self.assertEqual(booking3.valid_dates(), False)
        booking4 = Booking(user=user1, room=room2, check_in=date.today() + timedelta(2), check_out=date.today() + timedelta(6))
        self.assertEqual(booking4.valid_dates(), True)
        booking5 = Booking(user=user1, room=room2, check_in=date.today(), check_out=date.today() + timedelta(6))
        self.assertEqual(booking5.valid_dates(), True)

class QueryTests(TestCase):
    def setUp(self):
        hotel = Hotel(hotel_name="Test Hotel", location="Test Location", contact=22, email="test@test.com")
        hotel.save()

        user1 = User(user_name="user1", email="user1@test.com", password="password", mobile=1234567890)
        user1.save()
        client1 = Client(user=user1, age=20, address="Test Address")
        client1.save()
        user2 = User(user_name="user2", email="user2@test.com", password="password", mobile=1234567890)
        user2.save()
        client2 = Client(user=user2, age=20, address="Test Address")
        client2.save()
        user3 = User(user_name="user3", email="user3@test.com", password="password", mobile=1234567890)
        user3.save()
        client3 = Client(user=user3, age=20, address="Test Address")
        client3.save()
        user4 = User(user_name="staff1", email="staff1@test.com", password="password", mobile=1234567890)
        user4.save()
        staff1 = Staff(user=user4, hotel=hotel)
        staff1.save()

        query1 = Query(user=client1, hotel=hotel, date=date.today(), subject="Query", query="Test Query 1", status=False)
        query1.save()
        query2 = Query(user=client2, hotel=hotel, date=date.today(), subject="Query", query="Test Query 2", status=False)
        query2.save()
        query3 = Query(user=client3, hotel=hotel, date=date.today(), subject="Query", query="Test Query 3", status=False)
        query3.save()
        query4 = Query(user=client1, hotel=hotel, date=date.today(), subject="Query", query="Test Query 4", status=True)
        query4.save()
        query5 = Query(user=client2, hotel=hotel, date=date.today(), subject="Query", query="Test Query 5", status=True)
        query5.save()

        feedback1 = Feedback(query=query4, feedback="Test Feedback 1", staff=staff1, date=date.today())
        feedback1.save()
        feedback2 = Feedback(query=query5, feedback="Test Feedback 2", staff=staff1, date=date.today())
        feedback2.save()

    def test_get_queries(self):
        #GET all queries and users
        staff = User.objects.get(user_name="staff1")
        staff = Staff.objects.get(user=staff)

        hotel = Hotel.objects.get(hotel_name="Test Hotel")

        #Get all queries for this hotel
        queries = hotel.get_unanswered_queries()
        self.assertEqual(queries.count(), 3)

        self.assertEqual(queries[0].status, False)
        self.assertEqual(queries[1].status, False)
        self.assertEqual(queries[2].status, False)

    def test_sendfeedback(self):
        #GET all queries and users
        staff = User.objects.get(user_name="staff1")
        staff = Staff.objects.get(user=staff)

        hotel = Hotel.objects.get(hotel_name="Test Hotel")

        #Get all queries for this hotel
        queries = hotel.get_unanswered_queries()
        self.assertEqual(queries.count(), 3)

        #Send feedback to the user
        feedback = Feedback(query=queries[0], feedback="Test Feedback", staff=staff, date=date.today())
        feedback.send_feedback()
        
        #successful feedback will set status to True
        self.assertEqual(feedback.query.status, True)







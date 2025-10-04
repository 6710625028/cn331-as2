from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Room, Booking


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.password = "12345"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "username": self.username,
            "password": self.password
        })
        self.assertRedirects(response, reverse("rooms"))

    def test_login_fail(self):
        response = self.client.post(reverse("login"), {
            "username": "wrong",
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')


class RoomBookingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "booker"
        self.password = "12345"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.room = Room.objects.create(name="Room A", capacity=5)

    def test_rooms_page_requires_login(self):
        response = self.client.get(reverse("rooms"))
        self.assertEqual(response.status_code, 302)  # redirect ไป login

    def test_book_room_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse("book_room", args=[self.room.id]), {
            "date": "2025-10-05",
            "time": "10:00"
        })
        self.assertRedirects(response, reverse("rooms"))
        self.assertTrue(Booking.objects.filter(room=self.room, user=self.user).exists())

    def test_book_room_invalid_data(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse("book_room", args=[self.room.id]), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "กรุณากรอกข้อมูลให้ถูกต้อง")

    def test_book_room_not_logged_in(self):
        response = self.client.post(reverse("book_room", args=[self.room.id]), {
            "date": "2025-10-05",
            "time": "10:00"
        })
        self.assertEqual(response.status_code, 302)

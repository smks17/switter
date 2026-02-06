from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AuthTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")

    def test_signup_user(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_user(self):
        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

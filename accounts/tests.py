from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com",
            username="testuser",
            phone="+995555111222",
            password="TestPassword123",
            recovery_question="What is your nickname?",
            recovery_answer="tester",
        )

    def test_register_user(self):
        data = {
            "email": "new@gmail.com",
            "username": "newuser",
            "phone": "+995555333444",
            "password": "NewPassword123",
            "password_confirm": "NewPassword123",
            "recovery_question": "What is your pet name?",
            "recovery_answer": "bubu",
        }

        response = self.client.post("/api/accounts/register/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="new@gmail.com").exists())

    def test_login_user(self):
        data = {
            "email": "test@gmail.com",
            "password": "TestPassword123",
        }

        response = self.client.post("/api/accounts/login/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_requires_authentication(self):
        response = self.client.get("/api/accounts/profile/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_view_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/accounts/profile/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_email_verification(self):
        cache.set("email_verification_test@gmail.com", "1234", timeout=3600)

        data = {
            "email": "test@gmail.com",
            "code": "1234",
        }

        response = self.client.post("/api/accounts/verify-email/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_email_verified)

    def test_recovery_request(self):
        data = {
            "email": "test@gmail.com",
            "recovery_answer": "tester",
        }

        response = self.client.post("/api/accounts/recovery/request/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("code", response.data)

    def test_recovery_confirm(self):
        cache.set("password_recovery_test@gmail.com", "1234", timeout=3600)

        data = {
            "email": "test@gmail.com",
            "code": "1234",
            "new_password": "NewPassword12345",
        }

        response = self.client.post("/api/accounts/recovery/confirm/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPassword12345"))
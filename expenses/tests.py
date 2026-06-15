from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Expense

User = get_user_model()


class ExpenseTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@gmail.com",
            username="user1",
            phone="+995555111111",
            password="TestPassword123",
            recovery_question="Question?",
            recovery_answer="answer",
        )

        self.user2 = User.objects.create_user(
            email="user2@gmail.com",
            username="user2",
            phone="+995555222222",
            password="TestPassword123",
            recovery_question="Question?",
            recovery_answer="answer",
        )

        self.category = Category.objects.create(
            user=self.user1,
            name="Food",
        )

    def test_create_category(self):
        self.client.force_authenticate(user=self.user1)

        data = {
            "name": "Transport",
        }

        response = self.client.post("/api/expenses/categories/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Category.objects.filter(user=self.user1, name="Transport").exists()
        )

    def test_create_expense(self):
        self.client.force_authenticate(user=self.user1)

        data = {
            "category": self.category.id,
            "title": "Lunch",
            "amount": "25.50",
            "date": "2026-06-15",
            "description": "Restaurant lunch",
        }

        response = self.client.post("/api/expenses/expenses/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Expense.objects.filter(user=self.user1, title="Lunch").exists()
        )

    def test_user_can_see_only_own_expenses(self):
        Expense.objects.create(
            user=self.user1,
            category=self.category,
            title="Lunch",
            amount="25.50",
            date="2026-06-15",
            description="User 1 expense",
        )

        self.client.force_authenticate(user=self.user2)

        response = self.client.get("/api/expenses/expenses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
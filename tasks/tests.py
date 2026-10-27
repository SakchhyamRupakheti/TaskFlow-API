from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class TaskAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPass123!"
        )

    def test_unauthenticated_user_cannot_list_tasks(self):
        response = self.client.get("/api/tasks/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
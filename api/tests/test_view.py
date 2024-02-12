from rest_framework.exceptions import ErrorDetail
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError

from api.models import DataModel, Tag, Custom_User


class UserRegisterTestCase(APITestCase):
    def test_user_register(self):
        url = reverse("api:register")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Custom_User.objects.count(), 1)
        self.assertEqual(Custom_User.objects.get().username, "testuser")
        self.assertTrue(Custom_User.objects.get().check_password("testpassword"))


class UserLoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

    def test_user_login(self):
        url = reverse("api:login")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        self.client.force_login(self.user)
        url = reverse("api:logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid(self):
        url = reverse("api:login")
        data = {"username": "invaliduser", "password": "invalidpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DataViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        # self.client.force_login(self.user)
        self.client.post(
            reverse("api:login"),
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.tag = Tag.objects.create(name="Tag1")
        self.data_model = DataModel.objects.create(
            user=self.user,
            SKU="ABC123",
            name="Test Product",
            category="Test Category",
            stock_status="In Stock",
            available_stock="10",
        )
        self.data_model.tags.add(self.tag)

    def test_data_read(self):
        url = reverse("api:data")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_create(self):
        url = reverse("api:data")
        data = {
            "SKU": "DEF456",
            "name": "New Product",
            "category": "New Category",
            "stock_status": "Out of Stock",
            "available_stock": "0",
            "tags": [{"name": "tag1", "name": "tag2"}],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DataModel.objects.count(), 2)
        self.assertEqual(DataModel.objects.last().name, "New Product")

    def test_data_read_unauthenticated(self):
        # self.client.logout()
        self.client.get(reverse("api:logout"))
        url = reverse("api:data")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

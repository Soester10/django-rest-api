from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework.exceptions import ErrorDetail

from api.models import Tag, DataModel, Custom_User
from api.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    TagSerializer,
    DataSerializer,
)


class UserSerializerTestCase(TestCase):
    def test_user_register_serializer_create(self):
        serializer = UserRegisterSerializer(
            data={
                "email": "test@example.com",
                "password": "testpassword",
                "username": "testuser",
            }
        )
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, get_user_model())

    def test_user_login_serializer_validate(self):
        Custom_User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        serializer = UserLoginSerializer(
            data={"username": "testuser", "password": "testpassword"}
        )
        self.assertTrue(serializer.is_valid())
        user = serializer.validate({"username": "testuser", "password": "testpassword"})
        self.assertIsInstance(user, get_user_model())


class DataSerializerTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        self.tag1 = Tag.objects.create(name="Tag1")
        self.tag2 = Tag.objects.create(name="Tag2")

        self.data_instance = DataModel.objects.create(
            user=self.user,
            SKU="ABC123",
            name="Product1",
            category="Category1",
            stock_status="In Stock",
            available_stock="20",
        )
        self.data_instance.tags.add(self.tag1, self.tag2)

    def test_data_serializer_read(self):
        serializer = DataSerializer(instance=self.data_instance)
        serialized_data = serializer.data
        self.assertEqual(serialized_data["SKU"], "ABC123")
        self.assertEqual(serialized_data["name"], "Product1")
        self.assertEqual(serialized_data["category"], "Category1")
        self.assertEqual(serialized_data["stock_status"], "In Stock")
        self.assertEqual(serialized_data["available_stock"], "20")
        self.assertEqual(len(serialized_data["tags"]), 2)
        self.assertIn({"name": "Tag1"}, serialized_data["tags"])
        self.assertIn({"name": "Tag2"}, serialized_data["tags"])


class TagSerializerTestCase(TestCase):
    def test_tag_serializer(self):
        serializer = TagSerializer(data={"name": "Test Tag"})
        self.assertTrue(serializer.is_valid())

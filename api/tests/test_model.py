from django.test import TestCase
from api.models import Custom_User, Tag, DataModel

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = Custom_User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.superuser = Custom_User.objects.create_superuser(
            email='admin@example.com',
            username='adminuser',
            password='adminpassword'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)

    def test_superuser_creation(self):
        self.assertEqual(self.superuser.email, 'admin@example.com')
        self.assertEqual(self.superuser.username, 'adminuser')
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_staff)

class TagModelTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Tag')

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Tag')

class DataModelTestCase(TestCase):
    def setUp(self):
        self.user = Custom_User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.tag1 = Tag.objects.create(name='Tag1')
        self.tag2 = Tag.objects.create(name='Tag2')
        self.data_model = DataModel.objects.create(
            user=self.user,
            SKU='ABC123',
            name='Test Product',
            category='Test Category',
            stock_status='In Stock',
            available_stock='10'
        )
        self.data_model.tags.add(self.tag1)
        self.data_model.tags.add(self.tag2)


    def test_data_model_creation(self):
        self.assertEqual(self.data_model.user, self.user)
        self.assertEqual(self.data_model.SKU, 'ABC123')
        self.assertEqual(self.data_model.name, 'Test Product')
        self.assertEqual(self.data_model.category, 'Test Category')
        self.assertEqual(self.data_model.stock_status, 'In Stock')
        self.assertEqual(self.data_model.available_stock, '10')
        self.assertEqual(self.data_model.tags.count(), 2)
        self.assertEqual(self.data_model.tags.first().name, 'Tag1')

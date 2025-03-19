from django.test import TestCase

from pages.models import User
from pages.views import UserRegistrationForm


# Create your tests here.
class UserModelTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            display_name='Test User',
            role=User.UserRole.CUSTOMER,
            balance=133.7
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, User.UserRole.CUSTOMER)
        self.assertEqual(user.balance, 133.7)
        self.assertTrue(user.check_password('testpassword'))

    def test_invalid_user_creation_without_username(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='',
                password='testpassword',
            )

    def test_invalid_user_creation_without_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='testuser',
                password='',
            )

class UserRegistrationFormTests(TestCase):
    def test_valid_form(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


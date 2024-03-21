from django.test import TestCase
from account.forms import (
    UserRegistrationForm,
    UserLoginForm
)


class TestUserRegistrationForm(TestCase):
    def test_valid_data(self):
        form = UserRegistrationForm(
            data={
                'username': 'benyamin',
                'email': 'beni@gmail.com',
                'password1': '1234',
                'password2': '1234',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class TestUserLoginForm(TestCase):
    def test_valid_data(self):
        form = UserLoginForm(
            data={
                'username': 'beni',
                'password': '1234',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_empty_data(self):
        form = UserLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

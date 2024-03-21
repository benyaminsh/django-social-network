from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from account.forms import UserRegistrationForm, UserLoginForm
from account.models import Relation


class TestUserRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_view_GET(self):
        request = self.client.get(reverse('account:user_register'))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'account/register.html')
        self.failUnless(request.context['form'], UserRegistrationForm)

    def test_user_register_view_POST(self):
        request = self.client.post(
            reverse('account:user_register'),
            data={
                'username': 'beni',
                'email': 'benitekser@gmail.com',
                'password1': '1234abcd',
                'password2': '1234abcd',
            }
        )
        self.assertRedirects(request, reverse('home:home'))
        self.assertEqual(User.objects.count(), 1)


class TestUserLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )

    def test_user_login_view_GET(self):
        request = self.client.get(reverse('account:user_login'))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'account/login.html')
        self.failUnless(request.context['form'], UserLoginForm)

    def test_user_login_view_POST(self):
        request = self.client.post(
            reverse('account:user_login'),
            data={
                'username': 'beni',
                'password': '1234',
            }
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, reverse('home:home'))


class TestUserLogoutView(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )
        self.client.login(
            username=user.username,
            email=user.email,
            password='1234'
        )

    def test_user_logout_view_GET(self):
        request = self.client.get(reverse('account:user_logout'))
        self.assertRedirects(request, reverse('home:home'))


class TestUserProfileView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )
        self.client.login(
            username=self.user.username,
            email=self.user.email,
            password='1234'
        )

    def test_user_profile_view_GET(self):
        request = self.client.get(reverse('account:user_profile', args=(self.user.id,)))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'account/profile.html')
        self.failUnless(request.context['user'], self.user)


class TestUserFollowView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )
        self.client.login(
            username=self.user.username,
            email=self.user.email,
            password='1234'
        )

    def test_user_follow_view_GET(self):
        new_user = User.objects.create_user(
            username='kevin',
            email='kevin@gmail.com',
            password='1234'
        )
        request = self.client.get(reverse('account:user_follow', args=(new_user.id,)))
        self.assertTrue(Relation.objects.filter(from_user=self.user, to_user=new_user).exists())
        self.assertRedirects(request, reverse('account:user_profile', args=(new_user.id,)))


class UserUnfollowView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )
        self.client.login(
            username=self.user.username,
            email=self.user.email,
            password='1234'
        )

    def test_user_unfollow_view_GET(self):
        new_user = User.objects.create_user(
            username='kevin',
            email='kevin@gmail.com',
            password='1234'
        )
        request = self.client.get(reverse('account:user_unfollow', args=(new_user.id,)))
        self.assertFalse(Relation.objects.filter(from_user=self.user, to_user=new_user).exists())
        self.assertRedirects(request, reverse('account:user_profile', args=(new_user.id,)))

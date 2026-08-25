from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from shop.models import Product, Profile


class ProfileTests(TestCase):
    def test_profile_created_on_register_flow(self):
        user = User.objects.create_user('alice', password='pass12345')
        Profile.objects.create(user=user, city='Москва')
        self.assertEqual(user.profile.city, 'Москва')

    def test_profile_page_requires_login(self):
        response = Client().get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_logged_in_user_sees_profile(self):
        user = User.objects.create_user('alice', password='pass12345')
        Profile.objects.create(user=user, city='Москва')
        client = Client()
        client.login(username='alice', password='pass12345')
        response = client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Москва')

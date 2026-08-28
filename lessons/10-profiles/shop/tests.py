from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from shop.models import Profile


class HomePageTests(TestCase):
    def test_home_page(self):
        response = Client().get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class ProfileTests(TestCase):
    def test_profile_created_on_register_flow(self):
        client = Client()
        response = client.post(
            reverse('register'),
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(username='alice')
        self.assertTrue(Profile.objects.filter(user=user).exists())

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

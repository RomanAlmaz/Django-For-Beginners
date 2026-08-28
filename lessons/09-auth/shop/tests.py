from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from shop.models import Product, Review


class HomePageTests(TestCase):
    def test_home_page(self):
        response = Client().get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class RegistrationTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        client = Client()
        response = client.post(
            reverse('register'),
            {
                'username': 'newbie',
                'email': 'newbie@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(username='newbie')
        self.assertEqual(user.email, 'newbie@example.com')
        self.assertEqual(int(client.session['_auth_user_id']), user.pk)


class LoginRequiredTests(TestCase):
    def test_product_create_redirects_anonymous_user_to_login(self):
        response = Client().get(reverse('product_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_logged_in_user_can_open_product_create(self):
        user = User.objects.create_user('buyer', password='pass12345')
        client = Client()
        client.login(username='buyer', password='pass12345')
        response = client.get(reverse('product_create'))
        self.assertEqual(response.status_code, 200)


class ReviewModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Книга', price=Decimal('10.00'))

    def test_rating_must_be_between_1_and_5(self):
        review = Review(
            product=self.product,
            author_name='Тест',
            rating=10,
            text='Слишком высокая оценка',
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

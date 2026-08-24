from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from shop.models import Product, Review


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

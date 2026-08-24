from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from shop.models import Product, Profile, Review


class ProfileTests(TestCase):
    def test_user_has_profile_after_creation(self):
        user = User.objects.create_user('alice', password='pass12345')
        Profile.objects.create(user=user, city='Москва')
        self.assertEqual(user.profile.city, 'Москва')


class ReviewOwnershipTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Книга', price=Decimal('10.00'))
        self.owner = User.objects.create_user('owner', password='pass12345')
        self.other = User.objects.create_user('other', password='pass12345')
        Profile.objects.create(user=self.owner)
        Profile.objects.create(user=self.other)
        self.review = Review.objects.create(
            product=self.product,
            user=self.owner,
            rating=5,
            text='Отличный товар',
        )

    def test_owner_can_open_review_edit(self):
        client = Client()
        client.login(username='owner', password='pass12345')
        url = reverse(
            'review_update',
            kwargs={'pk': self.product.pk, 'review_pk': self.review.pk},
        )
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_other_user_gets_404_on_review_edit(self):
        client = Client()
        client.login(username='other', password='pass12345')
        url = reverse(
            'review_update',
            kwargs={'pk': self.product.pk, 'review_pk': self.review.pk},
        )
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_any_logged_in_user_can_edit_product(self):
        """Товары без проверки владельца - намеренно, см. README урока."""
        client = Client()
        client.login(username='other', password='pass12345')
        url = reverse('product_update', kwargs={'pk': self.product.pk})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

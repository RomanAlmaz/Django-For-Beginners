from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from shop.models import Product, Profile, Review


class HomePageTests(TestCase):
    def test_home_page(self):
        response = Client().get(reverse('home'))
        self.assertEqual(response.status_code, 200)


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
        self.edit_url = reverse(
            'review_update',
            kwargs={'pk': self.product.pk, 'review_pk': self.review.pk},
        )
        self.delete_url = reverse(
            'review_delete',
            kwargs={'pk': self.product.pk, 'review_pk': self.review.pk},
        )

    def test_anonymous_redirected_to_login_on_edit(self):
        response = Client().get(self.edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_anonymous_redirected_to_login_on_delete(self):
        response = Client().get(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_owner_can_edit(self):
        client = Client()
        client.login(username='owner', password='pass12345')
        response = client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)

    def test_owner_can_submit_edit(self):
        client = Client()
        client.login(username='owner', password='pass12345')
        response = client.post(
            self.edit_url,
            {'rating': 4, 'text': 'Обновлённый отзыв'},
        )
        self.assertEqual(response.status_code, 302)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.text, 'Обновлённый отзыв')

    def test_other_user_gets_404_on_edit(self):
        client = Client()
        client.login(username='other', password='pass12345')
        response = client.get(self.edit_url)
        self.assertEqual(response.status_code, 404)

    def test_other_user_post_cannot_change_review(self):
        client = Client()
        client.login(username='other', password='pass12345')
        response = client.post(
            self.edit_url,
            {'rating': 1, 'text': 'Взлом'},
        )
        self.assertEqual(response.status_code, 404)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 5)

    def test_owner_can_delete(self):
        client = Client()
        client.login(username='owner', password='pass12345')
        response = client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

    def test_owner_can_open_delete_confirmation(self):
        client = Client()
        client.login(username='owner', password='pass12345')
        response = client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

    def test_other_user_gets_404_on_delete_get(self):
        client = Client()
        client.login(username='other', password='pass12345')
        response = client.get(self.delete_url)
        self.assertEqual(response.status_code, 404)

    def test_other_user_gets_404_on_delete_post(self):
        client = Client()
        client.login(username='other', password='pass12345')
        response = client.post(self.delete_url)
        self.assertEqual(response.status_code, 404)

    def test_any_logged_in_user_can_edit_product(self):
        """Товары без ownership - намеренно, см. README Lesson 09."""
        client = Client()
        client.login(username='other', password='pass12345')
        url = reverse('product_update', kwargs={'pk': self.product.pk})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

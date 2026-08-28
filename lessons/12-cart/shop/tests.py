from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from shop.cart import (
    MAX_CART_QUANTITY,
    add_to_cart,
    get_cart_item_count,
    is_product_in_cart,
    remove_from_cart,
    update_cart_item,
)
from shop.models import Product


class HomePageTests(TestCase):
    def test_home_page(self):
        response = Client().get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class CartLogicTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Книга', price=Decimal('10.00'))
        self.client = Client()

    def test_add_and_count(self):
        session = self.client.session
        add_to_cart(session, self.product.pk, 2)
        session.save()
        self.assertEqual(get_cart_item_count(self.client.session), 2)

    def test_update_and_remove(self):
        session = self.client.session
        add_to_cart(session, self.product.pk, 2)
        update_cart_item(session, self.product.pk, 5)
        session.save()
        self.assertEqual(get_cart_item_count(self.client.session), 5)
        remove_from_cart(session, self.product.pk)
        session.save()
        self.assertEqual(get_cart_item_count(self.client.session), 0)

    def test_quantity_clamped_to_max(self):
        session = self.client.session
        add_to_cart(session, self.product.pk, MAX_CART_QUANTITY + 50)
        session.save()
        self.assertEqual(get_cart_item_count(self.client.session), MAX_CART_QUANTITY)

    def test_invalid_quantity_defaults_to_one(self):
        session = self.client.session
        add_to_cart(session, self.product.pk, -5)
        session.save()
        self.assertEqual(get_cart_item_count(self.client.session), 1)

    def test_invalid_product_key_is_removed(self):
        session = self.client.session
        session['cart'] = {str(self.product.pk): 2, 'abc': 1}
        session.save()
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_cart_item_count(self.client.session), 2)

    def test_update_zero_removes_item(self):
        session = self.client.session
        add_to_cart(session, self.product.pk, 3)
        session.save()
        update_cart_item(session, self.product.pk, 0)
        session.save()
        self.assertEqual(get_cart_item_count(self.client.session), 0)

    def test_update_negative_removes_item(self):
        session = self.client.session
        add_to_cart(session, self.product.pk, 3)
        session.save()
        update_cart_item(session, self.product.pk, -5)
        session.save()
        self.assertEqual(get_cart_item_count(self.client.session), 0)

    def test_deleted_product_removed_from_count(self):
        session = self.client.session
        add_to_cart(session, self.product.pk, 3)
        session.save()
        self.product.delete()
        self.assertEqual(get_cart_item_count(self.client.session), 0)

    def test_is_product_in_cart(self):
        session = self.client.session
        self.assertFalse(is_product_in_cart(session, self.product.pk))
        add_to_cart(session, self.product.pk, 2)
        session.save()
        self.assertTrue(is_product_in_cart(self.client.session, self.product.pk))

    def test_cart_page_shows_total(self):
        session = self.client.session
        add_to_cart(session, self.product.pk, 2)
        session.save()
        response = self.client.get(reverse('cart'))
        self.assertContains(response, 'Книга')
        self.assertContains(response, '20')

    def test_cart_add_requires_post(self):
        url = reverse('cart_add', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_cart_add_via_post(self):
        url = reverse('cart_add', kwargs={'pk': self.product.pk})
        response = self.client.post(url, {'quantity': 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_cart_item_count(self.client.session), 2)

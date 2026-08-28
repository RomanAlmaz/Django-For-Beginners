from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
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
from shop.models import Order, OrderItem, Product, Profile
from shop.orders import create_order_from_cart


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


class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('buyer', password='pass12345')
        Profile.objects.create(user=self.user)
        self.other = User.objects.create_user('other', password='pass12345')
        Profile.objects.create(user=self.other)
        self.product = Product.objects.create(name='Книга', price=Decimal('10.00'))
        self.client = Client()
        self.client.login(username='buyer', password='pass12345')

    def _add_product_to_session(self, quantity=2):
        session = self.client.session
        add_to_cart(session, self.product.pk, quantity)
        session.save()

    def test_create_order_from_cart(self):
        session = self.client.session
        add_to_cart(session, self.product.pk, 2)
        session.save()

        order = create_order_from_cart(self.user, session)
        session.save()

        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total, Decimal('20.00'))
        self.assertEqual(order.status, Order.STATUS_NEW)
        self.assertEqual(order.items.count(), 1)
        item = order.items.get()
        self.assertEqual(item.product_name, 'Книга')
        self.assertEqual(item.price, Decimal('10.00'))
        self.assertEqual(item.quantity, 2)
        self.assertEqual(get_cart_item_count(self.client.session), 0)

    def test_order_item_keeps_price_snapshot(self):
        self.product.price = Decimal('100.00')
        self.product.save()

        session = self.client.session
        add_to_cart(session, self.product.pk, 1)
        session.save()

        order = create_order_from_cart(self.user, session)
        self.assertIsNotNone(order)

        self.product.price = Decimal('150.00')
        self.product.save()

        item = order.items.get()
        self.assertEqual(item.price, Decimal('100.00'))
        self.assertEqual(item.product_name, 'Книга')
        self.assertEqual(order.total, Decimal('100.00'))

    def test_create_order_from_empty_cart_returns_none(self):
        order = create_order_from_cart(self.user, self.client.session)
        self.assertIsNone(order)

    def test_large_valid_cart_total_fits_order_field(self):
        expensive_product = Product.objects.create(
            name='Дорогой товар',
            price=Decimal('99999999.99'),
        )
        session = self.client.session
        add_to_cart(session, expensive_product.pk, MAX_CART_QUANTITY)

        order = create_order_from_cart(self.user, session)

        self.assertEqual(order.total, Decimal('9899999999.01'))

    def test_order_error_keeps_cart_and_rolls_back_database(self):
        session = self.client.session
        add_to_cart(session, self.product.pk, 2)

        with patch(
            'shop.orders.OrderItem.objects.create',
            side_effect=RuntimeError('test error'),
        ):
            with self.assertRaises(RuntimeError):
                create_order_from_cart(self.user, session)

        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(get_cart_item_count(session), 2)

    def test_checkout_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_checkout_empty_cart_redirects(self):
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('cart'))

    def test_checkout_post_empty_cart_redirects(self):
        response = self.client.post(reverse('checkout'))
        self.assertRedirects(response, reverse('cart'))
        self.assertEqual(Order.objects.count(), 0)

    def test_checkout_creates_order(self):
        self._add_product_to_session(3)
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total, Decimal('30.00'))
        self.assertEqual(get_cart_item_count(self.client.session), 0)
        self.assertRedirects(response, reverse('order_detail', kwargs={'pk': order.pk}))

    def test_order_detail_shows_items(self):
        self._add_product_to_session(2)
        self.client.post(reverse('checkout'))
        order = Order.objects.get(user=self.user)
        response = self.client.get(reverse('order_detail', kwargs={'pk': order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Книга')
        self.assertContains(response, '20')

    def test_other_user_cannot_view_order(self):
        self._add_product_to_session(1)
        self.client.post(reverse('checkout'))
        order = Order.objects.get(user=self.user)

        self.client.logout()
        self.client.login(username='other', password='pass12345')
        response = self.client.get(reverse('order_detail', kwargs={'pk': order.pk}))
        self.assertEqual(response.status_code, 404)

    def test_order_list_shows_only_own_orders(self):
        self._add_product_to_session(1)
        self.client.post(reverse('checkout'))
        own_order = Order.objects.get(user=self.user)
        other_order = Order.objects.create(
            user=self.other,
            total=Decimal('15.00'),
        )

        response = self.client.get(reverse('order_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse('order_detail', kwargs={'pk': own_order.pk}),
        )
        self.assertNotContains(
            response,
            reverse('order_detail', kwargs={'pk': other_order.pk}),
        )

    def test_cannot_delete_product_that_is_in_an_order(self):
        self._add_product_to_session(1)
        self.client.post(reverse('checkout'))

        url = reverse('product_delete', kwargs={'pk': self.product.pk})
        response = self.client.post(url)
        self.assertRedirects(
            response,
            reverse('product_detail', kwargs={'pk': self.product.pk}),
        )
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_product_detail_hides_delete_link_when_in_order(self):
        delete_url = reverse('product_delete', kwargs={'pk': self.product.pk})
        detail_url = reverse('product_detail', kwargs={'pk': self.product.pk})
        before = self.client.get(detail_url)
        self.assertContains(before, delete_url)

        self._add_product_to_session(1)
        self.client.post(reverse('checkout'))

        after = self.client.get(detail_url)
        self.assertNotContains(after, delete_url)

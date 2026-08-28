from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from shop.models import Product


class ProductPageTests(TestCase):
    def test_featured_product_appears_on_home_page(self):
        Product.objects.create(
            name='Книга',
            price=Decimal('10.00'),
            is_featured=True,
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Книга')

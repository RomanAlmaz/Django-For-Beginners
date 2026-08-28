from decimal import Decimal

from django.test import TestCase

from shop.models import Product


class ProductModelTests(TestCase):
    def test_product_can_be_created(self):
        product = Product.objects.create(
            name='Книга',
            price=Decimal('10.00'),
        )

        self.assertEqual(product.name, 'Книга')
        self.assertEqual(str(product), 'Книга')

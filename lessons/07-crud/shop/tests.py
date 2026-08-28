from django.test import TestCase
from django.urls import reverse

from shop.models import Product


class ProductCreateTests(TestCase):
    def test_product_can_be_created_from_form(self):
        response = self.client.post(
            reverse('product_create'),
            {
                'name': 'Книга',
                'price': '10.00',
                'description': 'Учебная книга',
                'is_featured': False,
            },
        )

        product = Product.objects.get(name='Книга')
        self.assertRedirects(
            response,
            reverse('product_detail', kwargs={'pk': product.pk}),
        )

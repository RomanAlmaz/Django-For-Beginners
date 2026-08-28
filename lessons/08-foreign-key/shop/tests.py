from decimal import Decimal

from django.test import TestCase

from shop.models import Category, Product, Review


class ForeignKeyTests(TestCase):
    def test_product_and_review_use_reverse_relations(self):
        category = Category.objects.create(name='Книги')
        product = Product.objects.create(
            category=category,
            name='Django для начинающих',
            price=Decimal('10.00'),
        )
        review = Review.objects.create(
            product=product,
            author_name='Анна',
            rating=5,
            text='Понятная книга',
        )

        self.assertEqual(category.products.get(), product)
        self.assertEqual(product.reviews.get(), review)

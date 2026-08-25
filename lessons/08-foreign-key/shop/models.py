from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField('название', max_length=100)
    description = models.TextField('описание', blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='категория',
    )
    name = models.CharField('название', max_length=200)
    price = models.DecimalField(
        'цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    description = models.TextField('описание', blank=True)
    is_featured = models.BooleanField('рекомендуемый', default=False)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='товар',
    )
    author_name = models.CharField('имя автора', max_length=100)
    rating = models.PositiveSmallIntegerField(
        'оценка',
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1.'),
            MaxValueValidator(5, message='Оценка не может быть больше 5.'),
        ],
    )
    text = models.TextField('текст отзыва')
    created_at = models.DateTimeField('дата', auto_now_add=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} о {self.product.name}'

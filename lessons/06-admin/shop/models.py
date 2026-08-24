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
    name = models.CharField('название', max_length=200)
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)
    description = models.TextField('описание', blank=True)
    is_featured = models.BooleanField('рекомендуемый', default=False)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name']

    def __str__(self):
        return self.name

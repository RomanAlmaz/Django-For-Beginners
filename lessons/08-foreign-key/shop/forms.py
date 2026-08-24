from django import forms

from shop.models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'description', 'is_featured']
        labels = {
            'category': 'Категория',
            'name': 'Название',
            'price': 'Цена',
            'description': 'Описание',
            'is_featured': 'Рекомендуемый',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'text']
        labels = {
            'author_name': 'Имя',
            'rating': 'Оценка',
            'text': 'Текст отзыва',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

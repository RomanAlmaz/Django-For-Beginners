from django import forms

from shop.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'is_featured']
        labels = {
            'name': 'Название',
            'price': 'Цена',
            'description': 'Описание',
            'is_featured': 'Рекомендуемый',
        }

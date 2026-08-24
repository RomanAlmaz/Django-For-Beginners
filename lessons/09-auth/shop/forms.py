from django import forms
from django.contrib.auth.forms import UserCreationForm

from shop.models import Product, Review


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)
        labels = {
            'username': 'Имя пользователя',
            'email': 'Почта',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].help_text = 'Обязательное поле. До 150 символов.'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password1'].help_text = (
            'Минимум 8 символов. Пароль не должен быть слишком простым.'
        )
        self.fields['password2'].help_text = 'Повторите пароль для проверки.'


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
        fields = ['rating', 'text']
        labels = {
            'rating': 'Оценка',
            'text': 'Текст отзыва',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

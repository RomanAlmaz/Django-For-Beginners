from django.shortcuts import render

from shop.models import Category, Product


def home(request):
    context = {
        'page_title': 'Главная',
        'welcome_message': (
            'Добро пожаловать в Django Shop! Это главная страница нашего магазина.'
        ),
        'categories': Category.objects.all(),
        'featured_products': Product.objects.filter(is_featured=True),
    }
    return render(request, 'shop/home.html', context)


def products(request):
    context = {
        'page_title': 'Товары',
        'products': Product.objects.all(),
    }
    return render(request, 'shop/products.html', context)


def about(request):
    context = {
        'page_title': 'О сайте',
        'about_text': (
            'Django Shop - учебный проект для пошагового изучения Django.'
        ),
        'team_members': [
            'Roman - автор курса',
            'Django - наш любимый фреймворк',
        ],
    }
    return render(request, 'shop/about.html', context)


def contact(request):
    context = {
        'page_title': 'Контакты',
        'contact_text': (
            'Свяжитесь с нами по вопросам курса или проекта Django Shop.'
        ),
        'email': 'hello@djangoshop.example',
    }
    return render(request, 'shop/contact.html', context)

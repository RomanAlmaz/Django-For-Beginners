from django.shortcuts import render


def home(request):
    context = {
        'page_title': 'Главная',
        'welcome_message': (
            'Добро пожаловать в Django Shop! Это главная страница нашего магазина.'
        ),
        'featured_products': [
            {'name': 'Кружка Python', 'price': '12.99'},
            {'name': 'Футболка Django', 'price': '24.99'},
            {'name': 'Стикеры для кодинга', 'price': '5.99'},
        ],
    }
    return render(request, 'shop/home.html', context)


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

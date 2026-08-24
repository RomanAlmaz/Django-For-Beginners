from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "Добро пожаловать в Django Shop! Это главная страница нашего магазина."
    )


def about(request):
    return HttpResponse(
        "Django Shop - учебный проект для пошагового изучения Django."
    )


def contact(request):
    return HttpResponse(
        "Свяжитесь с нами: hello@djangoshop.example (демо-страница для обучения)."
    )

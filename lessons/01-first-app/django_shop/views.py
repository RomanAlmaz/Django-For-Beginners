from django.http import HttpResponse


def hello(request):
    return HttpResponse("Привет, Django! Добро пожаловать в Django Shop.")

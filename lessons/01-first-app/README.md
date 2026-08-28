# Lesson 01 - First View

Первый урок курса Django for Beginners. Вы продолжите проект из Lesson 00 и добавите **одну** простую страницу.

## Что нужно знать до урока

Как запустить проект из Lesson 00 и где находится `django_shop/urls.py`.

## Что не нужно запоминать

Внутреннее устройство HTTP. Достаточно понять: URL вызывает view, а view возвращает ответ.

## Что изучается в этом уроке

- view (представление);
- `HttpResponse`;
- URL routing;
- `path()`.

## Запуск

Автор курса использует **Python 3.14.3** и **Django 5.2.12**. Если virtual environment ещё не создан:

**Windows (Command Prompt):**

```bat
py -m venv venv
venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Что уже было в Lesson 00

В прошлом уроке вы:

- создали пустой Django project `django_shop`;
- запустили development server;
- увидели стандартную страницу Django с ракетой на `/`.

## Что добавляется в этом уроке

Мы напишем первую view-функцию и подключим её к главной странице. Без приложений, без шаблонов - только текст в браузере.

## Структура проекта

```
01-first-app/
├── manage.py
├── requirements.txt
├── README.md
└── django_shop/
    ├── settings.py
    ├── urls.py
    ├── views.py      # новый файл
    ├── wsgi.py
    └── asgi.py
```

## Шаг 1. Первый view

View (представление) - Python-функция, которая получает HTTP-запрос и возвращает HTTP-ответ.

Создайте файл `django_shop/views.py`:

```python
from django.http import HttpResponse


def hello(request):
    return HttpResponse("Привет, Django! Добро пожаловать в Django Shop.")
```

`HttpResponse` - простой способ вернуть текст в браузер. Позже мы будем использовать HTML-шаблоны.

## Шаг 2. URL routing

В `django_shop/urls.py` подключите URL к view:

```python
from django.contrib import admin
from django.urls import path

from django_shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello, name='hello'),
]
```

- `path('', ...)` - главная страница сайта (`http://127.0.0.1:8000/`);
- `name='hello'` - имя URL для использования в шаблонах и ссылках позже.

## Шаг 3. Проверка и запуск

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

Откройте в браузере: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Вы должны увидеть текст: `Привет, Django! Добро пожаловать в Django Shop.`

Ракеты больше нет - вместо неё ваша первая страница.

## Проверь себя

1. Какая функция вызывается при открытии `/`?
2. Что возвращает `HttpResponse`?
3. Как имя view связано с записью в `urlpatterns`?

## Итог урока

Вы написали первую view-функцию, подключили URL и получили рабочую страницу на главном адресе сайта.

## Домашнее задание

1. Измените текст в `hello` view на свой собственный.
2. Добавьте вторую view `about` с коротким текстом о проекте Django Shop.
3. Подключите её по адресу `/about/`.

## После этого урока

Вы должны уметь:

- объяснить, что такое view;
- создать простую view с `HttpResponse`;
- подключить URL к view через `path()`;
- отличить пустой проект (Lesson 00) от проекта с первой страницей.

## Следующий урок

[Lesson 02 - URLs](../02-urls/README.md)

## Предыдущий урок

[Lesson 00 - Hello Django](../00-hello-django/README.md)

# Lesson 02 - URLs

Второй урок курса Django for Beginners. Вы продолжите проект из Lesson 01 и настроите несколько URL-адресов для страниц магазина.

## Что нужно знать до урока

Что такое view, `HttpResponse` и `path()`.

## Что не нужно запоминать

Назначение всех файлов, созданных `startapp`. В этом уроке нужны только `views.py`, `urls.py` и `apps.py`.

## Что изучается в этом уроке

- project vs app;
- `startapp`;
- `INSTALLED_APPS`;
- views в приложении;
- URL routing на двух уровнях;
- `include()`;
- `HttpResponse`.

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

## Что уже было в Lesson 01

В прошлом уроке вы:

- создали Django project `django_shop`;
- написали одну view-функцию `hello` в `django_shop/views.py`;
- подключили главную страницу через `path()`.

## Что добавляется в этом уроке

Теперь мы создаем **app** (приложение) `shop` и переносим страницы магазина в него. Так Django-проекты обычно организуют код: проект отвечает за общие настройки, а приложения - за конкретные части сайта.

## Project vs App

| | Project | App |
|---|---------|-----|
| Пример | `django_shop` | `shop` |
| Роль | Настройки всего сайта, главный `urls.py` | Одна функциональная часть: views, URLs, модели |
| Создание | `django-admin startproject` | `python manage.py startapp` |

Один project может содержать несколько apps. В нашем магазине позже появятся отдельные части: каталог, корзина, заказы.

## Структура проекта

```
02-urls/
├── manage.py
├── requirements.txt
├── README.md
├── django_shop/          # project
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── shop/                 # app
    ├── apps.py
    ├── views.py
    ├── urls.py
    └── ...
```

## Шаг 1. Создание приложения

Команда для создания app:

```bash
python manage.py startapp shop
```

Django создаст папку `shop` с базовыми файлами. В этом уроке мы используем:

- `views.py` - view-функции;
- `urls.py` - URL-адреса приложения (файл создаем вручную);
- `apps.py` - конфигурация приложения.

Django также создаёт пустые `models.py`, `admin.py` и `tests.py`. Сейчас их менять не нужно: модели появятся в Lesson 05, админка - в Lesson 06, тесты - позже.

## Шаг 2. Регистрация app в INSTALLED_APPS

Django должен знать о новом приложении. Откройте `django_shop/settings.py` и добавьте `shop`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'shop',
]
```

`INSTALLED_APPS` - список всех приложений, которые Django загружает при запуске.

## Шаг 3. Views в приложении shop

В `shop/views.py` создайте три view-функции:

```python
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
```

Каждая view получает `request` (данные HTTP-запроса) и возвращает `HttpResponse` (текст для браузера).

View из Lesson 01 больше не нужна. Удалите `django_shop/views.py`: теперь страницы магазина живут только в приложении `shop`. Это оставляет одно понятное место для view-функций.

## Шаг 4. URL routing в приложении

Создайте файл `shop/urls.py`:

```python
from django.urls import path

from shop import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
```

Здесь:

- `''` - главная страница (`/`);
- `'about/'` - страница «О сайте» (`/about/`);
- `'contact/'` - страница «Контакты» (`/contact/`);
- `name` - уникальное имя URL внутри приложения.

## Шаг 5. Подключение URLs приложения к проекту

В `django_shop/urls.py` подключите URLs приложения через `include`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]
```

`include('shop.urls')` говорит Django: "все URL с корня сайта обрабатывает приложение shop".

## Шаг 6. Проверка и запуск

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

Откройте в браузере:

| URL | Страница |
|-----|----------|
| [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Главная |
| [http://127.0.0.1:8000/about/](http://127.0.0.1:8000/about/) | О сайте |
| [http://127.0.0.1:8000/contact/](http://127.0.0.1:8000/contact/) | Контакты |

## Проверь себя

1. Чем project отличается от app?
2. Зачем нужен `include('shop.urls')`?
3. Почему view магазина теперь находятся в `shop/views.py`?

## Итог урока

Вы создали Django app, зарегистрировали его, добавили несколько view-функций и настроили URL routing на двух уровнях: project и app.

## Домашнее задание

1. Добавьте страницу `help/` с коротким текстом о том, как пользоваться магазином.
2. Создайте view `faq` и подключите ее по адресу `/faq/`.
3. Попробуйте изменить текст на одной из страниц и убедиться, что сервер показывает новый текст (Django перезагружает код автоматически при `runserver`).

## После этого урока

Вы понимаете:

- что такое URLconf и как URL попадает во view;
- как работает `path()`;
- зачем нужен `include()` для подключения URLs приложения;
- разницу между project и app.

Вы должны уметь:

- создать app через `startapp` и добавить в `INSTALLED_APPS`;
- организовать URLs в `app/urls.py`;
- подключить app URLs через `include()` в project `urls.py`.

## Следующий урок

[Lesson 03 - Templates](../03-templates/README.md)

## Предыдущий урок

[Lesson 01 - First View](../01-first-app/README.md)

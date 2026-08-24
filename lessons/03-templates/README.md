# Lesson 03 - Templates

Четвертый урок курса Django for Beginners. Вы продолжите проект из Lesson 02 и замените простой текст на HTML-шаблоны.

## Что изучается в этом уроке

- templates (шаблоны);
- `render()`;
- context (контекст);
- переменные шаблона `{{ variable }}`;
- `{% if %}`;
- `{% for %}`;
- наследование шаблонов;
- `base.html`;
- `{% extends %}` и `{% block %}`;
- `{% url %}`.

## Запуск

```bash
py -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py runserver
```

## Что уже было в Lesson 02

В прошлом уроке вы:

- создали приложение `shop`;
- добавили три view с `HttpResponse`;
- настроили URL routing через `include()`.

Страницы показывали только голый текст без HTML-разметки.

## Что добавляется в этом уроке

Мы переносим HTML в шаблоны и передаем данные из view через **context**.

## Порядок изучения шаблонов

Изучайте по шагам, не всё сразу:

1. `render()` и `{{ variable }}` - данные из view в HTML.
2. `{% if %}` и `{% for %}` - условия и циклы.
3. `{% extends %}` и `{% block %}` - общий `base.html`.
4. `{% url %}` - ссылки по имени URL.

### Зачем `{% url %}` вместо `/about/`

Плохо (жёсткий путь):

```html
<a href="/about/">О сайте</a>
```

Если URL изменится в `urls.py`, все ссылки в шаблонах нужно править вручную.

Хорошо:

```html
<a href="{% url 'about' %}">О сайте</a>
```

Django строит путь из `name='about'` в `urls.py`. Одно место правды.

## Что такое template

Template (шаблон) - HTML-файл с дополнительными тегами Django. View передает данные в шаблон, а шаблон формирует финальную HTML-страницу для браузера.

Вместо:

```python
return HttpResponse("Hello")
```

мы используем:

```python
return render(request, 'shop/home.html', context)
```

`render()` - функция Django, которая берет шаблон, подставляет данные из context и возвращает готовый HTML.

## Структура проекта

```
03-templates/
├── manage.py
├── django_shop/
└── shop/
    ├── views.py
    ├── urls.py
    └── templates/
        └── shop/
            ├── base.html
            ├── home.html
            ├── about.html
            └── contact.html
```

Django ищет шаблоны в папке `templates/` внутри каждого приложения. Путь `shop/templates/shop/home.html` соответствует имени шаблона `shop/home.html`.

## Шаг 1. Базовый шаблон base.html

Создайте `shop/templates/shop/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Django Shop{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Django Shop</h1>
        <nav>
            <a href="{% url 'home' %}">Home</a>
            |
            <a href="{% url 'about' %}">About</a>
            |
            <a href="{% url 'contact' %}">Contact</a>
        </nav>
    </header>

    <main>
        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <p>Django Shop - learning project</p>
    </footer>
</body>
</html>
```

- `{% block title %}` и `{% block content %}` - области, которые дочерние шаблоны могут переопределить;
- `{% url 'home' %}` - Django строит ссылку по имени URL из `urls.py`.

## Шаг 2. Шаблон home.html

Создайте `shop/templates/shop/home.html`:

```html
{% extends 'shop/base.html' %}

{% block title %}{{ page_title }} - Django Shop{% endblock %}

{% block content %}
    <h2>{{ page_title }}</h2>
    <p>{{ welcome_message }}</p>

    <h3>Featured products</h3>
    {% if featured_products %}
        <ul>
            {% for product in featured_products %}
                <li>{{ product.name }} - ${{ product.price }}</li>
            {% endfor %}
        </ul>
    {% else %}
        <p>New products coming soon.</p>
    {% endif %}
{% endblock %}
```

Здесь:

- `{% extends 'shop/base.html' %}` - шаблон наследует общую структуру;
- `{{ page_title }}` - переменная из context;
- `{% if featured_products %}` - условие: список не пустой;
- `{% for product in featured_products %}` - цикл по списку товаров.

## Шаг 3. View с render() и context

Обновите `shop/views.py`:

```python
from django.shortcuts import render


def home(request):
    context = {
        'page_title': 'Home',
        'welcome_message': (
            'Welcome to Django Shop! This is the home page of our online store.'
        ),
        'featured_products': [
            {'name': 'Python Mug', 'price': '12.99'},
            {'name': 'Django T-Shirt', 'price': '24.99'},
            {'name': 'Coding Stickers', 'price': '5.99'},
        ],
    }
    return render(request, 'shop/home.html', context)
```

**Context** - словарь Python. Ключи словаря становятся переменными в шаблоне.

## Шаг 4. Шаблоны about и contact

`shop/templates/shop/about.html`:

```html
{% extends 'shop/base.html' %}

{% block title %}{{ page_title }} - Django Shop{% endblock %}

{% block content %}
    <h2>{{ page_title }}</h2>
    <p>{{ about_text }}</p>

    {% if team_members %}
        <h3>Our team</h3>
        <ul>
            {% for member in team_members %}
                <li>{{ member }}</li>
            {% endfor %}
        </ul>
    {% endif %}
{% endblock %}
```

`shop/templates/shop/contact.html`:

```html
{% extends 'shop/base.html' %}

{% block title %}{{ page_title }} - Django Shop{% endblock %}

{% block content %}
    <h2>{{ page_title }}</h2>
    <p>{{ contact_text }}</p>
    <p>Email: {{ email }}</p>
{% endblock %}
```

## Шаг 5. Остальные view

Добавьте в `shop/views.py` функции `about` и `contact` с `render()` и своим context. Пример для `about`:

```python
def about(request):
    context = {
        'page_title': 'About',
        'about_text': (
            'About Django Shop: a beginner-friendly project to learn Django step by step.'
        ),
        'team_members': [
            'Alex - course author',
            'Django - our favorite framework',
        ],
    }
    return render(request, 'shop/about.html', context)
```

## Шаг 6. Проверка и запуск

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

Откройте в браузере:

| URL | Что вы увидите |
|-----|----------------|
| [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Home с навигацией и списком товаров |
| [http://127.0.0.1:8000/about/](http://127.0.0.1:8000/about/) | About с списком team members |
| [http://127.0.0.1:8000/contact/](http://127.0.0.1:8000/contact/) | Contact с email из context |

На всех страницах общий header, nav и footer из `base.html`.

## Итог урока

Вы научились отделять HTML от Python-кода: view передает данные через context, а шаблоны формируют страницу. Общие части сайта живут в `base.html`, а каждая страница расширяет его через `{% extends %}`.

## Домашнее задание

1. Добавьте в context на главной странице поле `store_open` (True/False) и в шаблоне покажите "Store is open" или "Store is closed" через `{% if %}`.
2. Добавьте четвертый товар в `featured_products` и проверьте, что он появился в списке.
3. Создайте шаблон `help.html` и страницу `/help/` с коротким текстом помощи (используйте `extends` и `render`).

## После этого урока

Вы должны уметь:

- объяснить, что такое Django template;
- использовать `render(request, template, context)`;
- передавать данные в шаблон через context;
- выводить переменные через `{{ variable }}`;
- использовать `{% if %}` и `{% for %}`;
- создать `base.html` и расширять его через `{% extends %}` и `{% block %}`;
- строить ссылки через `{% url %}`.

## Следующий урок

[Lesson 04 - Static Files](../04-static/README.md)

## Предыдущий урок

[Lesson 02 - URLs](../02-urls/README.md)

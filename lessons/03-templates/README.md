# Lesson 03 - Templates

Третий урок курса Django for Beginners. Вы продолжите проект из Lesson 02 и замените простой текст на HTML-шаблоны.

## Что нужно знать до урока

Как view связана с URL, а также базовые HTML-теги.

## Что не нужно запоминать

Все template tags сразу. Проходите урок по мини-этапам и возвращайтесь к примерам.

## Что изучается в этом уроке

**Основное** (это нужно пройти):

- templates (шаблоны);
- `render()`;
- context (контекст);
- переменные шаблона `{{ variable }}`;
- `{% extends %}` и `{% block %}`.

**Дополнительно** (можно прочитать после рабочего примера):

- template tags: `{% if %}`, `{% for %}`, `{% url %}`;
- filters;
- CSRF (краткий взгляд вперёд).

## Маршрут урока

Сначала только основное. Не пытайтесь запомнить все теги сразу.

| Этап | Сначала понять |
|------|----------------|
| 1 | `render()` открывает HTML-шаблон |
| 2 | context передаёт данные, `{{ variable }}` выводит их |
| 3 | `base.html`, `{% extends %}` и `{% block %}` убирают копирование общего HTML |

`{% if %}`, `{% for %}`, `{% url %}`, filters и CSRF разобраны в блоке **Дополнительно**. В готовых шаблонах урока они уже есть: сначала скопируйте, затем прочитайте объяснение.

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

## Что уже было в Lesson 02

В прошлом уроке вы:

- создали приложение `shop`;
- добавили три view с `HttpResponse`;
- настроили URL routing через `include()`.

Страницы показывали только голый текст без HTML-разметки.

## Что добавляется в этом уроке

Мы переносим HTML в шаблоны и передаем данные из view через **context**.

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
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django Shop{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Django Shop</h1>
        <nav>
            <a href="{% url 'home' %}">Главная</a>
            <a href="{% url 'about' %}">О сайте</a>
            <a href="{% url 'contact' %}">Контакты</a>
        </nav>
    </header>

    <main>
        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <p>Django Shop - учебный проект. Создано: Roman</p>
    </footer>
</body>
</html>
```

- `{% block title %}` и `{% block content %}` - области, которые дочерние шаблоны могут переопределить;
- `{% url 'home' %}` уже стоит в навигации. Как он работает, разберём в блоке **Дополнительно**.

## Шаг 2. Шаблон home.html

Создайте `shop/templates/shop/home.html`:

```html
{% extends 'shop/base.html' %}

{% block title %}{{ page_title }} - Django Shop{% endblock %}

{% block content %}
    <h2>{{ page_title }}</h2>
    <p>{{ welcome_message }}</p>

    <h3>Избранные товары</h3>
    {% if featured_products %}
        <ul>
            {% for product in featured_products %}
                <li>{{ product.name }} - {{ product.price }} руб.</li>
            {% endfor %}
        </ul>
    {% else %}
        <p>Скоро появятся новые товары.</p>
    {% endif %}
{% endblock %}
```

Здесь основное:

- `{% extends 'shop/base.html' %}` - шаблон наследует общую структуру;
- `{% block title %}` и `{% block content %}` - заполняют области из `base.html`;
- `{{ page_title }}` - переменная из context.

`{% if %}` и `{% for %}` в этом файле разберём в блоке **Дополнительно**.

## Шаг 3. View с render() и context

Обновите `shop/views.py`:

```python
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
        <h3>Наша команда</h3>
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
    <p><strong>Почта:</strong> {{ email }}</p>
{% endblock %}
```

## Шаг 5. Остальные view

Добавьте в `shop/views.py` функции `about` и `contact` с `render()` и своим context. Пример для `about`:

```python
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
| [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Главная с навигацией и списком товаров |
| [http://127.0.0.1:8000/about/](http://127.0.0.1:8000/about/) | Страница «О сайте» со списком участников |
| [http://127.0.0.1:8000/contact/](http://127.0.0.1:8000/contact/) | Контакты с email из context |

На всех страницах общий header, nav и footer из `base.html`.

## Дополнительно

Этот блок не обязателен, чтобы страницы заработали. Он помогает прочитать теги, которые уже стоят в шаблонах урока.

### Template tags: `{% if %}`, `{% for %}`, `{% url %}`

В `home.html` уже есть условие и цикл:

- `{% if featured_products %}` - показать список, только если он не пустой;
- `{% for product in featured_products %}` - повторить разметку для каждого товара.

В `base.html` ссылки построены так:

```html
<a href="{% url 'about' %}">О сайте</a>
```

Плохо (жёсткий путь):

```html
<a href="/about/">О сайте</a>
```

Если URL изменится в `urls.py`, все такие ссылки нужно править вручную. `{% url 'about' %}` берёт путь из `name='about'`. Одно место правды.

### Filters

В шаблоне можно изменить значение перед выводом:

```html
{{ product.name|upper }}
```

`upper` - filter: делает буквы заглавными. На этом уроке filters не нужны. Запомните только: `{{ variable }}` выводит значение, `|filter` меняет его. Подробнее встретите позже.

### CSRF: взгляд вперёд

Когда появится HTML-форма с POST (логин, отзыв, корзина), Django потребует скрытое поле `{% csrf_token %}`. Это защита от поддельных запросов с чужого сайта.

Сейчас форм с POST в уроке нет, поэтому CSRF можно не настраивать. Просто знайте имя тега: вы увидите его в следующих уроках.

## Проверь себя

1. Что передаёт словарь `context` в шаблон?
2. Зачем нужны `base.html`, `{% extends %}` и `{% block %}`?
3. Чем `{% if %}` отличается от `{% for %}`? (блок **Дополнительно**)

## Итог урока

Вы научились отделять HTML от Python-кода: view передает данные через context, а шаблоны формируют страницу. Общие части сайта живут в `base.html`, а каждая страница расширяет его через `{% extends %}`.

## Домашнее задание

1. Добавьте в context на главной странице поле `store_open` (`True` / `False`) и через `{% if %}` покажите «Магазин открыт» или «Магазин закрыт» (см. блок **Дополнительно**).
2. Добавьте четвертый товар в `featured_products` и проверьте, что он появился в списке.
3. Создайте шаблон `help.html` и страницу `/help/` с коротким текстом помощи (используйте `extends` и `render`).

## После этого урока

Вы должны уметь:

- объяснить, что такое Django template;
- использовать `render(request, template, context)`;
- передавать данные в шаблон через context;
- выводить переменные через `{{ variable }}`;
- создать `base.html` и расширять его через `{% extends %}` и `{% block %}`.

Если прочитали блок **Дополнительно**: читать `{% if %}`, `{% for %}` и `{% url %}` в готовом шаблоне.

## Следующий урок

[Lesson 04 - Static Files](../04-static/README.md)

## Предыдущий урок

[Lesson 02 - URLs](../02-urls/README.md)

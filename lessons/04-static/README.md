# Lesson 04 - Static Files

Четвертый урок курса Django for Beginners. Вы продолжите проект из Lesson 03 и подключите **статические файлы**: CSS, JavaScript и изображения.

## Что нужно знать до урока

Как устроены `base.html`, `{% extends %}` и `{% block %}`.

## Что не нужно запоминать

DOM API и весь CSS. Главная цель - понять, как Django находит и подключает static files.

## Что изучается в этом уроке

- static files (статические файлы);
- папка `static/`;
- `STATIC_URL`;
- `{% load static %}`;
- `{% static %}`;
- CSS;
- JavaScript;
- images.

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

## Что уже было в Lesson 03

В прошлом уроке вы:

- создали HTML-шаблоны с `{% extends %}` и `{% block %}`;
- передавали данные через context;
- использовали `{% if %}` и `{% for %}`.

Страницы работали, но выглядели как простой HTML без стилей.

## Что добавляется в этом уроке

Мы добавим CSS, JavaScript и логотип. Django будет раздавать эти файлы через встроенный механизм static files.

## Что такое static files

Static files - файлы, которые не генерируются Python-кодом: стили, скрипты, картинки, иконки.

Django не вставляет CSS в шаблон вручную. Шаблон только **ссылку** на файл, а Django находит файл в папке `static/`.

## Структура проекта

```
04-static/
└── shop/
    ├── static/
    │   └── shop/
    │       ├── css/
    │       │   └── style.css
    │       ├── js/
    │       │   └── main.js
    │       └── images/
    │           └── logo.svg
    └── templates/
        └── shop/
            └── base.html
```

Путь `shop/static/shop/css/style.css` соответствует `{% static 'shop/css/style.css' %}`.

## Шаг 1. CSS

Создайте `shop/static/shop/css/style.css` с базовыми стилями для header, nav, main и footer.

Сокращённый пример. В готовом `style.css` те же цвета вынесены в CSS variables, чтобы не повторять значения:

```css
body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #eef1f2;
}

.site-header {
    background: #334e5c;
    color: #fff;
    padding: 1rem 1.5rem;
}
```

## Шаг 2. JavaScript (минимальный пример)

Создайте `shop/static/shop/js/main.js`:

```javascript
const yearElement = document.querySelector('[data-current-year]');

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}
```

В footer есть элемент:

```html
<span data-current-year>2026</span>
```

После загрузки страницы JavaScript подставляет текущий год. Результат виден прямо на сайте.

Этот урок про **Django static files**, а не про DOM и JavaScript. Сейчас достаточно понять: браузер загрузил `main.js`, выполнил его и изменил HTML.

## Шаг 3. Изображение

Создайте `shop/static/shop/images/logo.svg` - простой логотип магазина.

## Шаг 4. Подключение в шаблоне

В начале `shop/templates/shop/base.html` добавьте:

```django
{% load static %}
```

Подключите CSS в `<head>`:

```html
<link rel="stylesheet" href="{% static 'shop/css/style.css' %}">
```

Логотип в header:

```html
<img src="{% static 'shop/images/logo.svg' %}" alt="Логотип Django Shop" width="40" height="40">
```

JavaScript перед закрывающим `</body>`:

```html
<script src="{% static 'shop/js/main.js' %}" defer></script>
```

Атрибут `defer` запускает скрипт после чтения HTML. Поэтому JavaScript сможет найти элемент footer.

### Важные теги

| Тег | Назначение |
|-----|------------|
| `{% load static %}` | Загружает тег `static` в шаблон |
| `{% static 'shop/css/style.css' %}` | URL к файлу в папке static |

## Шаг 5. STATIC_URL

В `django_shop/settings.py` уже есть:

```python
STATIC_URL = 'static/'
```

Это префикс URL для статических файлов в development mode. Приложение `django.contrib.staticfiles` уже в `INSTALLED_APPS`.

## Шаг 6. Проверка и запуск

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

Откройте [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Вы должны увидеть:

- тёмный серо-синий header с медной линией;
- стилизованную навигацию;
- белый блок контента на светло-сером фоне;
- текущий год в footer, который подставил JavaScript.

## Проверь себя

1. Чем static file отличается от HTML-шаблона?
2. Зачем в шаблоне нужен `{% load static %}`?
3. Как путь `shop/static/shop/css/style.css` связан с `{% static %}`?

## Итог урока

Вы научились хранить CSS, JS и images в папке `static/` и подключать их в шаблонах через `{% static %}`. Сайт выглядит как обычная веб-страница, а не голый HTML.

## Домашнее задание

1. Измените цвет header в `style.css` и проверьте, что стиль обновился после перезагрузки страницы.
2. Измените цвет текста в `.site-footer` и проверьте footer в браузере.
3. Замените текст в footer (`base.html`) на свой.

## После этого урока

Вы должны уметь:

- объяснить, что такое static files в Django;
- создать структуру `app/static/app/...`;
- использовать `{% load static %}` и `{% static %}`;
- подключить CSS, JavaScript и images в шаблон;
- понимать роль `STATIC_URL`.

## Следующий урок

[Lesson 05 - Models](../05-models/README.md)

## Предыдущий урок

[Lesson 03 - Templates](../03-templates/README.md)

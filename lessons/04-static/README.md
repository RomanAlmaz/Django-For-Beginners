# Lesson 04 - Static Files

Пятый урок курса Django for Beginners. Вы продолжите проект из Lesson 03 и подключите **статические файлы**: CSS, JavaScript и изображения.

## Что изучается в этом уроке

- static files (статические файлы);
- папка `static/`;
- `STATIC_URL`;
- `{% load static %}`;
- `{% static %}`;
- CSS;
- JavaScript;
- images.

## Окружение

Автор курса использует **Python 3.14.3** и **Django 5.2.12**.

```bash
py -m venv venv
```

**Windows (Git Bash):**

```bash
source venv/Scripts/activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
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

Пример:

```css
body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #f5f5f5;
}

.site-header {
    background: #092e20;
    color: #fff;
    padding: 1rem 1.5rem;
}
```

## Шаг 2. JavaScript (минимальный пример)

Создайте `shop/static/shop/js/main.js`:

```javascript
console.log('Django Shop: static JavaScript file loaded.');
```

Этот урок про **Django static files**, а не про JavaScript. Мы показываем, что Django может раздавать `.js` файлы так же, как CSS. Изучение JavaScript - отдельная тема.

Откройте DevTools в браузере (F12) → Console - увидите сообщение при загрузке страницы.

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
<img src="{% static 'shop/images/logo.svg' %}" alt="Django Shop logo" width="40" height="40">
```

JavaScript перед закрывающим `</body>`:

```html
<script src="{% static 'shop/js/main.js' %}" defer></script>
```

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

- зеленый header с логотипом;
- стилизованную навигацию;
- белый блок контента на сером фоне;
- в footer текущий год (из JavaScript).

## Итог урока

Вы научились хранить CSS, JS и images в папке `static/` и подключать их в шаблонах через `{% static %}`. Сайт выглядит как обычная веб-страница, а не голый HTML.

## Домашнее задание

1. Измените цвет header в `style.css` и проверьте, что стиль обновился после перезагрузки страницы.
2. Добавьте класс `.product-list` для списка товаров на главной странице.
3. В `main.js` добавьте `console.log('Django Shop loaded')` и откройте DevTools в браузере.

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

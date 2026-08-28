# Решение частых проблем

Сначала убедитесь, что терминал открыт в папке нужного урока:

```bash
pwd
ls
```

В этой папке должны быть `manage.py` и `requirements.txt`.

## `python: command not found` или `py: command not found`

Python не установлен или не добавлен в `PATH`.

Проверьте:

```bash
py --version
python3 --version
```

На Windows обычно работает `py`, на Linux и macOS - `python3`.

## `No module named django`

Virtual environment не активирован или зависимости не установлены:

**Windows (Command Prompt):**

```bat
py -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Другие варианты активации на Windows:

**PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Git Bash:**

```bash
source venv/Scripts/activate
```

Проверка:

```bash
python -m django --version
```

## `That port is already in use`

Порт `8000` занят другим процессом. Запустите сервер на другом порту:

```bash
python manage.py runserver 8001
```

Откройте `http://127.0.0.1:8001/`.

## `OperationalError: no such table`

Таблицы базы ещё не созданы:

```bash
python manage.py migrate
```

Запускайте команду внутри папки текущего урока.

## `TemplateDoesNotExist`

Проверьте три вещи:

1. Шаблон лежит в `shop/templates/shop/`.
2. В `render()` указан путь вроде `'shop/home.html'`.
3. Приложение `'shop'` есть в `INSTALLED_APPS`.

## `NoReverseMatch`

Django не нашёл URL по имени или не получил нужный параметр.

Сравните:

```python
path('products/<int:pk>/', views.product_detail, name='product_detail')
```

и:

```django
{% url 'product_detail' product.pk %}
```

Имя `product_detail` и параметр `pk` должны совпадать.

## `CSRF verification failed`

Каждая внутренняя POST-форма должна содержать:

```django
<form method="post">
    {% csrf_token %}
    ...
</form>
```

Не отключайте CSRF middleware ради исправления ошибки.

## `DoesNotExist` или страница 404

Проверьте, что объект с таким ID есть в базе. Для view обычно используйте:

```python
product = get_object_or_404(Product, pk=pk)
```

Тогда пользователь увидит страницу 404 вместо необработанной ошибки.

## Django просит создать новую миграцию

Проверьте состояние:

```bash
python manage.py makemigrations --check --dry-run
```

Если вы сами изменили модель в домашнем задании:

```bash
python manage.py makemigrations
python manage.py migrate
```

Не копируйте `db.sqlite3` между уроками. Каждый урок использует свою структуру моделей и миграций.

## CSS или JavaScript не обновились

1. Убедитесь, что в шаблоне есть `{% load static %}`.
2. Проверьте путь внутри `{% static 'shop/css/style.css' %}`.
3. Обновите страницу без кеша: `Ctrl+F5`.
4. Убедитесь, что `django.contrib.staticfiles` есть в `INSTALLED_APPS`.

## Если ошибка осталась

Выполните:

```bash
python manage.py check
```

Читайте последнюю часть traceback снизу вверх. Обычно последние строки содержат тип ошибки, файл и номер строки.

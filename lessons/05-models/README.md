# Lesson 05 - Models

Пятый урок курса Django for Beginners. Вы продолжите проект из Lesson 04 и добавите первые **модели** для магазина: `Category` и `Product`.

## Что нужно знать до урока

Базовые Python-классы, импорты, шаблоны и context.

## Что не нужно запоминать

SQL и все типы полей Django. Достаточно понять путь от класса модели до таблицы и ORM-запроса.

## Что изучается в этом уроке

Главная тема - **модели и миграции**:

- Django model и поля (`CharField`, `TextField`, `DecimalField`, …);
- `makemigrations` и `migrate`;
- SQLite и файл `db.sqlite3`;
- ORM: `objects.all()`, `objects.filter()`.

Цепочка для новичка:

```
Python class → Model → migration → таблица в базе → ORM → objects.all()
```

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

После `migrate` база существует, но записей в ней ещё нет. В **Lesson 06** мы научимся создавать категории и товары через Django Admin.

В этом уроке `shop/admin.py` пока пустой, поэтому модели ещё не видны в `/admin/`. Это не ошибка.

## Что уже было в Lesson 04

В прошлых уроках вы:

- создали приложение `shop` с шаблонами;
- использовали `render()` и context;
- подключили CSS, JavaScript и images через `{% static %}`;
- показывали список товаров из Python-словаря в view.

Данные жили только в коде. После перезапуска сервера они не менялись, но их нельзя было редактировать без правки Python-файла.

## Что добавляется в этом уроке

Мы создаем **модели** `Category` и `Product`. Django сохранит данные в базе SQLite и позволит получать их через ORM.

## Что такое Model

Model (модель) - Python-класс, который описывает структуру данных. Django автоматически создает таблицу в базе данных на основе модели.

Например, модель `Product` описывает товар: название, цена, описание.

## Структура проекта

```
05-models/
├── manage.py
├── django_shop/
└── shop/
    ├── models.py
    ├── views.py
    ├── fixtures/
    │   └── initial_data.json
    ├── migrations/
    │   └── 0001_initial.py
    └── templates/
        └── shop/
            ├── base.html
            ├── home.html
            ├── products.html
            └── ...
```

## Шаг 1. Модели Category и Product

Откройте `shop/models.py`:

```python
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField('название', max_length=100)
    description = models.TextField('описание', blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=200)
    price = models.DecimalField(
        'цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    description = models.TextField('описание', blank=True)
    is_featured = models.BooleanField('рекомендуемый', default=False)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name']

    def __str__(self):
        return self.name
```

### Поля моделей

| Поле | Тип | Назначение |
|------|-----|------------|
| `name` | `CharField` | Короткий текст (название) |
| `description` | `TextField` | Длинный текст |
| `price` | `DecimalField` | Число с десятичной точкой (цена). В коде урока - `MinValueValidator(0.01)`, чтобы цена не могла быть отрицательной (модель защищает данные, не только HTML-форма) |
| `is_featured` | `BooleanField` | True/False (товар на главной) |
| `created_at` | `DateTimeField` | Дата и время создания |

`blank=True` означает, что поле может быть пустым в формах. `auto_now_add=True` автоматически записывает время создания.

`__str__` - как объект отображается в админке и в shell (добавим админку в следующем уроке).

`MinValueValidator` запрещает цену меньше `0.01`. Подписи вроде `'название'` Django позже покажет в формах и админке.

## Шаг 2. Миграции

Миграция - файл, который описывает изменения в структуре базы данных.

Создайте миграции:

```bash
python manage.py makemigrations shop
```

Django создаст файл в `shop/migrations/`.

Примените миграции:

```bash
python manage.py migrate
```

Django создаст файл `db.sqlite3` и таблицы `shop_category` и `shop_product`.

## Шаг 3. Запросы к базе через ORM

ORM (Object-Relational Mapping) - способ работать с базой через Python-код, без SQL.

Обновите `shop/views.py`:

```python
from django.shortcuts import render

from shop.models import Category, Product


def home(request):
    context = {
        'page_title': 'Главная',
        'welcome_message': (
            'Добро пожаловать в Django Shop! Это главная страница нашего магазина.'
        ),
        'categories': Category.objects.all(),
        'featured_products': Product.objects.filter(is_featured=True),
    }
    return render(request, 'shop/home.html', context)


def products(request):
    context = {
        'page_title': 'Товары',
        'products': Product.objects.all(),
    }
    return render(request, 'shop/products.html', context)
```

### Основные запросы ORM

| Код | Что делает |
|-----|------------|
| `Category.objects.all()` | Все категории |
| `Product.objects.all()` | Все товары |
| `Product.objects.filter(is_featured=True)` | Только избранные товары |
| `Product.objects.get(pk=1)` | Один товар по id |

## Шаг 4. Шаблон products.html

Создайте `shop/templates/shop/products.html` - страница со всеми товарами из базы.

Добавьте URL в `shop/urls.py`:

```python
path('products/', views.products, name='products'),
```

И ссылку в навигации `base.html`:

```html
<a href="{% url 'products' %}">Товары</a>
```

На главной странице категории и избранные товары теперь приходят из базы, а не из словаря в view.

## Шаг 5. Проверка и запуск

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

Страницы `/` и `/products/` будут пустыми - это нормально. Данные появятся в Lesson 06 через Admin.

## 💡 Если хотите сразу получить готовые данные

См. [Test data](../../TEST_DATA.md) - опциональная загрузка `initial_data` через `loaddata`. Это **не** обязательная часть курса.

## 💡 Дополнительно: Django shell

```bash
python manage.py shell
```

```python
from shop.models import Product
Product.objects.all()
Product.objects.filter(price__gte=20)
```

Shell - интерактивная консоль Python с доступом к Django. Удобно для экспериментов, не обязательна на этом уроке.

## Первый простой тест

Тесты подробно появятся позже. Сейчас достаточно посмотреть на `shop/tests.py`: Django создаёт временную базу, создаёт `Product` и проверяет результат.

```bash
python manage.py test
```

## Проверь себя

1. Как Python-класс модели превращается в таблицу?
2. Чем `makemigrations` отличается от `migrate`?
3. Что возвращают `Product.objects.all()` и `.filter()`?

## Итог урока

Вы создали модели, применили миграции и научились получать записи из базы через `objects.all()` и `objects.filter()`. Данные магазина теперь живут в SQLite.

## Домашнее задание

1. Добавьте фильтр на странице products: товары с ценой меньше 20.
2. Добавьте поле `stock` (IntegerField) в модель Product и создайте миграцию.
3. (Опционально) Загрузите тестовые данные - см. [Test data](../../TEST_DATA.md).

## После этого урока

Вы должны уметь:

- объяснить, что такое Django model;
- создать модель с разными типами полей;
- выполнить `makemigrations` и `migrate`;
- получать данные через `objects.all()` и `objects.filter()`;
- понимать, где Django хранит данные (SQLite, файл `db.sqlite3`).

## Следующий урок

[Lesson 06 - Django Admin](../06-admin/README.md)

## Предыдущий урок

[Lesson 04 - Static Files](../04-static/README.md)

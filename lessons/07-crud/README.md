# Lesson 07 - CRUD

Седьмой урок курса Django for Beginners. Вы продолжите проект из Lesson 06 и добавите **CRUD** для товаров на публичном сайте: создание, чтение, обновление и удаление через формы.

## Что нужно знать до урока

Модели, ORM, view-функции, шаблоны и обычные HTML-формы.

## Что не нужно запоминать

Весь Forms API. Важно увидеть повторяющийся путь: показать форму, проверить POST, сохранить и сделать redirect.

## Что изучается в этом уроке

Главная тема - **CRUD**. `ModelForm`, GET, POST, validation, CSRF и redirect здесь выступают инструментами одного сценария, а не отдельными большими темами.

- Create, Read, Update, Delete (CRUD);
- Django forms;
- ModelForm;
- GET и POST;
- validation (валидация);
- CSRF;
- `get_object_or_404`;
- `redirect`.

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

## Что уже было в Lesson 06

В прошлом уроке вы:

- настроили Django Admin для `Category` и `Product`;
- управляли данными через `/admin/`.

Админка удобна для разработчика, но на реальном сайте пользователи и менеджеры часто работают через **свои страницы** с формами. В этом уроке мы строим такой интерфейс для товаров.

## Что добавляется в этом уроке

Полный CRUD для модели `Product` на сайте. **Важно:** на этом уроке страницы создания и редактирования **намеренно открыты всем** - мы учим CRUD без авторизации. В Lesson 09 мы закроем их через `login_required`.

| Операция | URL | Действие |
|----------|-----|----------|
| Read (список) | `/products/` | Все товары |
| Read (один) | `/products/1/` | Страница товара |
| Create | `/products/create/` | Форма добавления |
| Update | `/products/1/edit/` | Форма редактирования |
| Delete | `/products/1/delete/` | Подтверждение удаления |

## Что такое CRUD

CRUD - четыре базовые операции с данными:

- **Create** - создать записи;
- **Read** - прочитать (список или одну запись);
- **Update** - изменить;
- **Delete** - удалить.

Django Admin уже делает CRUD. Здесь мы реализуем то же для обычных страниц сайта.

## Структура проекта

```
07-crud/
└── shop/
    ├── forms.py              # ModelForm
    ├── views.py              # CRUD views
    ├── urls.py               # новые маршруты
    └── templates/shop/
        ├── product_detail.html
        ├── product_form.html
        └── product_confirm_delete.html
```

## Шаг 1. ModelForm

ModelForm - класс Django, который строит HTML-форму на основе модели.

Создайте `shop/forms.py`:

```python
from django import forms

from shop.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'is_featured']
```

Django автоматически создаст поля формы из полей модели `Product`.

## Шаг 2. View для чтения (Read)

**Список** - уже есть `products` view.

**Одна запись** - `product_detail`.

Нам приходит `pk` из URL. Первый очевидный вариант:

```python
product = Product.objects.get(pk=pk)
```

Если товара нет, `.get()` вызовет `DoesNotExist`. Для страницы сайта удобнее готовый helper `get_object_or_404()`: он ищет объект и возвращает обычную страницу 404, если запись не найдена.

```python
from django.shortcuts import get_object_or_404, render

from shop.models import Product


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'page_title': product.name,
        'product': product,
    }
    return render(request, 'shop/product_detail.html', context)
```

`pk` - primary key (id записи в базе). `get_object_or_404` возвращает объект или страницу 404.

## Шаг 3. View для создания (Create)

```python
from django.shortcuts import redirect

from shop.forms import ProductForm


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()

    context = {
        'page_title': 'Добавить товар',
        'form': form,
    }
    return render(request, 'shop/product_form.html', context)
```

### GET и POST

- **GET** - браузер открывает страницу, показываем пустую форму;
- **POST** - пользователь отправил форму, читаем `request.POST`, валидируем и сохраняем.

`form.is_valid()` проверяет данные (validation). Если все ок - `form.save()` создает записи в базе.

## Шаг 4. View для обновления (Update)

```python
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    context = {
        'page_title': 'Редактировать товар',
        'form': form,
        'product': product,
    }
    return render(request, 'shop/product_form.html', context)
```

`instance=product` говорит форме: редактируем существующий объект, а не создаем новый.

## Шаг 5. View для удаления (Delete)

```python
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('products')

    context = {
        'page_title': 'Удалить товар',
        'product': product,
    }
    return render(request, 'shop/product_confirm_delete.html', context)
```

Удаление через POST - безопасная практика. Ссылка GET не должна удалять данные.

## Шаг 6. URLs

Добавьте в `shop/urls.py`:

```python
path('products/create/', views.product_create, name='product_create'),
path('products/<int:pk>/', views.product_detail, name='product_detail'),
path('products/<int:pk>/edit/', views.product_update, name='product_update'),
path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
```

Путь `products/create/` должен быть **выше** `products/<int:pk>/`, чтобы Django не путал `create` с id.

## Шаг 7. Шаблон формы и CSRF

`shop/templates/shop/product_form.html`:

```html
<form method="post" class="product-form">
    {% csrf_token %}

    {% for field in form %}
        <div class="form-field">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {{ field }}
            {% if field.errors %}
                <div class="field-errors">{{ field.errors }}</div>
            {% endif %}
        </div>
    {% endfor %}

    <button type="submit">Сохранить</button>
</form>
```

**CSRF** (Cross-Site Request Forgery) - защита от поддельных POST-запросов. Тег `{% csrf_token %}` обязателен в каждой POST-форме. Без него Django вернет ошибку 403.

Тот же `{% csrf_token %}` нужен в форме удаления.

## Шаг 8. Проверка и запуск

```bash
python manage.py migrate
python manage.py runserver
```

Тестовые данные: через Admin или см. [Test data](../../TEST_DATA.md).

Попробуйте:

| URL | Действие |
|-----|----------|
| [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/) | Список и ссылка «Добавить товар» |
| [http://127.0.0.1:8000/products/create/](http://127.0.0.1:8000/products/create/) | Создать товар |
| [http://127.0.0.1:8000/products/1/](http://127.0.0.1:8000/products/1/) | Детали товара |
| [http://127.0.0.1:8000/products/1/edit/](http://127.0.0.1:8000/products/1/edit/) | Редактировать |
| [http://127.0.0.1:8000/products/1/delete/](http://127.0.0.1:8000/products/1/delete/) | Удалить |

Проверьте validation: отправьте форму с пустым name или отрицательной price.

## Простой тест CRUD

`shop/tests.py` отправляет POST на форму создания товара и проверяет redirect на новую страницу товара.

```bash
python manage.py test
```

## Проверь себя

1. Что `ModelForm` берёт из модели автоматически?
2. Почему GET показывает форму, а POST отправляет данные?
3. Зачем после сохранения нужен redirect и зачем форме нужен CSRF token?

## Итог урока

Вы реализовали CRUD для товаров на публичном сайте: ModelForm, обработка GET/POST, валидация, CSRF и redirect после успешных действий. Это основа для любых форм в Django.

## Домашнее задание

1. Добавьте CRUD для модели `Category` (список, create, edit, delete).
2. На странице товара покажите сообщение, если поле description пустое.
3. После удаления товара покажите flash message (подсказка: `django.contrib.messages`).

## После этого урока

Вы должны уметь:

- объяснить CRUD;
- создать ModelForm для модели;
- обрабатывать GET и POST в одной view;
- использовать `form.is_valid()` и `form.save()`;
- добавить `{% csrf_token %}` в формы;
- использовать `get_object_or_404` и `redirect`;
- настроить URL с параметром `<int:pk>`.

## Следующий урок

[Lesson 08 - ForeignKey](../08-foreign-key/README.md)

## Предыдущий урок

[Lesson 06 - Django Admin](../06-admin/README.md)

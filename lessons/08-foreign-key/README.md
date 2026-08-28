# Lesson 08 - ForeignKey

Восьмой урок курса Django for Beginners. Вы продолжите проект из Lesson 07 и добавите **ForeignKey**: категория для товара и отзывы на товар.

## Что нужно знать до урока

Модели, ORM, `ModelForm`, CRUD и `get_object_or_404()`.

## Что не нужно запоминать

Оптимизацию SQL и все типы связей. Сейчас нужны только `ForeignKey`, `on_delete` и `related_name`.

## Что изучается в этом уроке

В этом уроке мы изучим **ForeignKey** на двух реальных примерах:

- **Product → Category** - один товар принадлежит одной категории;
- **Review → Product** - один товар может иметь много отзывов.

Вы изучите:

- что такое связь между моделями;
- `ForeignKey`, `on_delete`, `related_name`;
- модель `Review` и обратные связи (`product.reviews.all()`, `category.products.all()`).

`OneToOneField` появится в Lesson 10 для профиля. `ManyToManyField` изучим позже, когда для него появится реальная задача.

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

Тестовые данные: через Admin (Lesson 06) или см. [Test data](../../TEST_DATA.md).

## Что уже было в Lesson 07

В прошлом уроке вы:

- реализовали CRUD для товаров;
- использовали ModelForm и POST-запросы.

Модели `Category` и `Product` существовали отдельно. Товар не знал свою категорию, отзывов не было.

## Что добавляется в этом уроке

1. **Product** связан с **Category** через ForeignKey.
2. Модель **Review** связана с **Product** через ForeignKey.
3. На странице товара отображаются отзывы и форма добавления отзыва.
4. На главной странице товары сгруппированы по категориям.

## Основная часть

```text
ForeignKey
    Product связан с Category
    Review связан с Product

related_name
    category.products
    product.reviews

ModelForm
    пользователь отправляет отзыв
```

Если вы впервые изучаете Django, пройдите только эту основную часть. Блок оптимизации ORM в конце можно полностью пропустить.

## Что такое связь между моделями

В реальном магазине:

- один товар принадлежит одной категории;
- один товар может иметь много отзывов.

В Django такие связи описываются полями **ForeignKey**.

## Структура проекта

```
08-foreign-key/
└── shop/
    ├── models.py           # Category, Product, Review
    ├── forms.py            # ProductForm + ReviewForm
    ├── migrations/
    │   └── 0002_product_category_review.py
    └── templates/shop/
        ├── home.html       # товары по категориям
        └── product_detail.html  # отзывы
```

## Шаг 1. ForeignKey Product -> Category

В `shop/models.py`:

```python
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
    )
    name = models.CharField(max_length=200)
    ...
```

### Важные параметры

| Параметр | Назначение |
|----------|------------|
| `ForeignKey` | Связь "много к одному" (много товаров - одна категория) |
| `on_delete=models.SET_NULL` | При удалении категории поле category станет NULL |
| `null=True, blank=True` | Категория необязательна |
| `related_name='products'` | Обратная связь: `category.products.all()` |

Без `related_name` Django создал бы имя `product_set` по умолчанию.

## Шаг 2. Модель Review

```python
class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} о {self.product.name}'
```

`on_delete=models.CASCADE` - при удалении товара удалятся все его отзывы.

Обратная связь: `product.reviews.all()` - все отзывы товара.

## Шаг 3. Миграции

```bash
python manage.py makemigrations shop
python manage.py migrate
```

Django создаст миграцию `0002_product_category_review.py`.

## Шаг 4. Обратные связи в шаблонах

На главной странице - товары внутри каждой категории:

```html
{% for category in categories %}
    <h4>{{ category.name }}</h4>
    {% for product in category.products.all %}
        <li>{{ product.name }}</li>
    {% endfor %}
{% endfor %}
```

`category.products.all()` работает благодаря `related_name='products'`.

На странице товара - отзывы:

```html
{% for review in product.reviews.all %}
    <li>{{ review.author_name }} - {{ review.rating }}/5</li>
{% endfor %}
```

## Шаг 5. Форма отзыва

`shop/forms.py`:

Сначала добавьте `category` в существующую форму товара:

```python
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'description', 'is_featured']
```

Затем создайте форму отзыва:

```python
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'text']
```

View `review_create` сохраняет отзыв и привязывает к товару:

```python
def review_create(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', pk=product.pk)
        return _render_product_detail(request, product, form)

    return redirect('product_detail', pk=product.pk)
```

`commit=False` нужен, потому что поля `product` нет в форме. Товар определяет сервер по URL:

```text
form.save()
    создать Review
    сразу сохранить в базу

form.save(commit=False)
    создать Review только в памяти
    добавить review.product на сервере
    вызвать review.save()
```

То есть `commit=False` не отменяет сохранение навсегда. Он даёт время добавить данные, которым нельзя доверять пользовательскую форму.

### Ошибки валидации формы

Если ученик отправит `rating=10`, Django **не** сохранит отзыв. Важно показать ошибку на странице:

```
POST
    ↓
form.is_valid()
    ↓
ошибки → снова render product_detail с form.errors
    ↓
успех → redirect
```

Без `return _render_product_detail(..., form)` форма просто исчезнет после неудачного POST. Шаблон `product_detail.html` уже выводит `field.errors` - view должен передать форму с ошибками.

## Шаг 6. Admin

В `shop/admin.py` зарегистрируйте `Review` и добавьте `category` в `list_display` для Product.

## Шаг 7. Проверка и запуск

```bash
python manage.py runserver
```

Проверьте:

| URL | Что смотреть |
|-----|--------------|
| [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Товары внутри категорий |
| [http://127.0.0.1:8000/products/1/](http://127.0.0.1:8000/products/1/) | Категория, отзывы, форма |
| [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | Review в админке |

Добавьте отзыв через форму на странице товара. Попробуйте отправить оценку **10** - форма должна остаться на странице с сообщением об ошибке.

## Валидация rating на уровне модели

В `shop/models.py` для поля `rating` используются валидаторы:

```python
from django.core.validators import MinValueValidator, MaxValueValidator

rating = models.PositiveSmallIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)],
)
```

После добавления валидаторов снова выполните:

```bash
python manage.py makemigrations shop
python manage.py migrate
```

Django создаст миграцию `0003_alter_review_rating.py`.

`min` и `max` в HTML-форме - только подсказка в браузере. **Серверная** проверка должна быть в модели или форме. Так Django не сохранит `rating=999`, даже если кто-то отправит запрос вручную.

## Дополнительно: оптимизация ORM

Этот блок можно пропустить. Сначала закрепите `product.category` и `category.products.all()`.

При большом количестве объектов Django может выполнить слишком много SQL-запросов. Для оптимизации существуют `select_related()` и `prefetch_related()`. В коде урока их намеренно нет: они будут отдельной темой после основ Django ORM.

## Простой тест ForeignKey

`shop/tests.py` создаёт категорию, товар и отзыв, а затем проверяет `category.products` и `product.reviews`.

```bash
python manage.py test
```

## Проверь себя

1. Что хранится в `Product.category`?
2. Зачем нужен `related_name='products'`?
3. Что произойдёт с товаром после удаления категории?
4. Почему `SET_NULL` требует `null=True`?

## Итог урока

Вы связали модели через ForeignKey, научились использовать обратные связи и добавили отзывы к товарам. Данные магазина теперь связаны так, как в реальном проекте.

## Домашнее задание

1. Сделайте категорию обязательной: уберите `blank=True` и `null=True`, создайте миграцию.
2. Отправьте отзыв с `rating=10` через форму на сайте - убедитесь, что Django показывает ошибку и форма не исчезает.
3. На странице `/products/` покажите количество отзывов у каждого товара (`product.reviews.count`).

## После этого урока

Вы должны уметь:

- объяснить ForeignKey и связь «много к одному»;
- использовать `on_delete` и `related_name`;
- получать связанные объекты через `product.reviews.all()` и `category.products.all()`;
- создать модель Review и связать с Product;
- обрабатывать ошибки формы: при `is_valid() == False` снова показать форму с `form.errors`;
- применить миграции после изменения моделей.

## Следующий урок

[Lesson 09 - Authentication](../09-auth/README.md)

## Предыдущий урок

[Lesson 07 - CRUD](../07-crud/README.md)

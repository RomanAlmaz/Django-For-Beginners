# Lesson 11 - Authorization (ownership)

Одиннадцатый урок курса Django for Beginners. Вы продолжите проект из Lesson 10 и добавите **authorization**: редактировать можно только свои отзывы.

**Главная тема урока:** **authorization** - может ли этот пользователь изменить **этот** объект?

## Что нужно знать до урока

Authentication, `request.user`, профили, отзывы и `get_object_or_404()`.

## Что не нужно запоминать

API исторических моделей миграций, сложные permissions и оптимизацию ORM. Главное - проверить владельца объекта.

## Что изучается в этом уроке

- authentication vs authorization;
- `review.user == request.user`;
- редактирование и удаление **только своих** отзывов;
- `raise Http404` при отказе в доступе.

Цепочка:

```
@login_required → вошёл?
    ↓
review.user == request.user? → разрешить / запретить
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

## Authentication vs Authorization

| | Authentication | Authorization |
|---|----------------|---------------|
| Вопрос | Кто вы? | Что вам разрешено? |
| Пример | `@login_required` | `if review.user != request.user` |

> **Напоминание:** CRUD товаров защищён только `@login_required`. Любой залогиненный пользователь может менять любой товар. Это **намеренно упрощённая** реализация - каталог считается «админским» контентом. `@login_required` **не** проверяет права на конкретный объект. Подробнее - в README Lesson 09.

## Новые и изменённые файлы

| Файл | Зачем |
|------|-------|
| `shop/models.py` | обязательная связь `Review.user` |
| `shop/admin.py` | отзывы только с пользователем |
| `shop/migrations/0005_review_user_only.py` | переход от `author_name` к `User` |
| `shop/views.py` | редактирование и удаление своих отзывов |
| `shop/urls.py` | URL для изменения и удаления |
| `shop/templates/shop/product_detail.html` | ссылки только для владельца |
| `shop/templates/shop/review_form.html` | форма редактирования |
| `shop/templates/shop/review_confirm_delete.html` | подтверждение удаления |
| `shop/tests.py` | проверки владельца и чужого доступа |

## Миграция 0005: отзывы только через User

**Продвинутая часть:** не нужно запоминать `apps.get_model()` и каждую строку миграции. Важно понять порядок: сначала подготовить старые данные, затем изменить структуру таблицы.

**Важно:** миграция `0005_review_user_only` удаляет отзывы **без** связанного `user`.

Эта миграция намеренно необратима: после удаления `author_name` Django не сможет восстановить старые имена автоматически. Перед подобной миграцией в реальном проекте делают резервную копию.

Почему Django не может автоматически превратить:

```
author_name = "Roman"
```

в:

```
user = ?
```

Django не знает, какому аккаунту принадлежит текстовое имя. В реальном проекте разработчик пишет **data migration**: сопоставляет `author_name` с `User` или назначает отзывы вручную.

В учебном проекте мы удаляем только отзывы **без** `user` перед тем, как сделать поле обязательным и убрать `author_name`.

Fixture `initial_data.json` с этого урока **не содержит отзывы**. Их нужно оставить на сайте после регистрации. Подробности: [TEST_DATA.md](../../TEST_DATA.md).

## Проверка владельца во view

```python
if review.user != request.user:
    raise Http404
```

Сначала view находит товар и отзыв. Затем сравнивает автора с текущим пользователем. Чужой пользователь получает 404 и не узнаёт, существует ли объект.

Альтернатива (показать в README, не обязательно в коде):

```python
review = get_object_or_404(
    Review,
    pk=review_pk,
    product=product,
    user=request.user,
)
```

## Редактирование и удаление

Для редактирования используется `ReviewForm(request.POST, instance=review)`. Параметр `instance` говорит Django обновить найденный отзыв.

Удаление выполняется только после POST. Обычный GET показывает страницу подтверждения:

```python
if request.method == 'POST':
    review.delete()
    return redirect('product_detail', pk=product.pk)
```

Новые URL:

```python
path(
    'products/<int:pk>/review/<int:review_pk>/edit/',
    views.review_update,
    name='review_update',
),
path(
    'products/<int:pk>/review/<int:review_pk>/delete/',
    views.review_delete,
    name='review_delete',
),
```

В `product_detail.html` ссылки «Изменить» и «Удалить» видит только автор:

```django
{% if review.user == user %}
    ...
{% endif %}
```

## Дополнительно: оптимизация ORM

Этот блок можно пропустить. Для темы ownership достаточно простого кода:

```python
product = get_object_or_404(Product, pk=pk)
```

При большом количестве связанных объектов Django иногда делает много SQL-запросов. Это называют проблемой N+1. Для её решения существуют `select_related()` и `prefetch_related()`.

В основном коде урока их нет: сначала важно понять связь объектов и проверку владельца. Оптимизацию ORM лучше изучить отдельно, когда обычные queryset уже понятны.

## Проверка

1. Оставьте отзыв - появятся «Изменить» / «Удалить».
2. Войдите другим пользователем - у чужого отзыва ссылок нет.
3. URL редактирования чужого отзыва - 404.

## Тесты

```bash
python manage.py test
```

Тесты проверяют редирект анонимного пользователя, GET и POST владельца, а также 404 для другого пользователя.

`test_any_logged_in_user_can_edit_product` намеренно фиксирует учебное упрощение Lesson 09. Это не пример правильных permissions для настоящего магазина.

## Проверь себя

1. Почему одного `@login_required` недостаточно для чужого отзыва?
2. Зачем при отказе мы возвращаем 404?
3. Почему данные нужно подготовить до удаления `author_name`?

## Итог урока

Authorization: только владелец может изменить свой отзыв.

## Домашнее задание

Не показывайте форму отзыва, если пользователь уже оставил отзыв на этот товар.

Подумайте: если форму скрыли только в шаблоне, пользователь всё равно может отправить POST вручную и создать второй отзыв. Как защитить это на уровне view или модели? (Подсказка: `UniqueConstraint` на `product` + `user` - тема для следующего шага, не для этого урока.)

## После этого урока

Вы должны уметь:

- объяснить разницу между authentication и authorization;
- проверить владельца: `review.user == request.user`;
- запретить редактирование чужих объектов;
- понимать, почему миграция данных иногда требует ручного решения.

## Следующий урок

[Lesson 12 - Cart](../12-cart/README.md)

## Предыдущий урок

[Lesson 10 - Profiles](../10-profiles/README.md)

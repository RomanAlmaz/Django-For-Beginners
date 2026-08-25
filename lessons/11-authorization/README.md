# Lesson 11 - Authorization (ownership)

**Главная тема урока:** **authorization** - может ли этот пользователь изменить **этот** объект?

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

```bash
py -m venv venv
source venv/Scripts/activate
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

## Миграция 0005: отзывы только через User

⚠️ **Важно:** миграция `0005_review_user_only` удаляет отзывы **без** связанного `user`.

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

## Проверка ownership

```python
if review.user != request.user:
    raise Http404
```

Альтернатива (показать в README, не обязательно в коде):

```python
review = get_object_or_404(
    Review,
    pk=review_pk,
    product=product,
    user=request.user,
)
```

## Проверка

1. Оставьте отзыв - появятся «Изменить» / «Удалить».
2. Войдите другим пользователем - у чужого отзыва ссылок нет.
3. URL редактирования чужого отзыва - 404.

## Тесты

```bash
python manage.py test
```

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

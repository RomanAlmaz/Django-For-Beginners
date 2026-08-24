# Lesson 10 - Profiles & Authorization (OneToOneField, ownership)

Одиннадцатый урок курса Django for Beginners.

> **Как проходить этот урок**
>
> Урок состоит из **двух независимых частей**. Не смешивайте их в одну «гигантскую тему»:
>
> 1. Сначала **Part 1 - Profile** (OneToOneField).
> 2. Затем **Part 2 - Authorization** (свои отзывы).
>
> Между частями можно сделать паузу и проверить Part 1 отдельно.

## Запуск

```bash
py -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Тестовые товары создайте через Admin (Lesson 06) или см. [Test data](../../TEST_DATA.md) для `loaddata`.

---

# Part 1 - Profile (OneToOneField)

**Тема этой части:** профиль пользователя. **Не** отзывы, **не** права доступа - только `Profile` и `OneToOneField`.

## Что изучаем в Part 1

- модель `Profile` с `OneToOneField` к `User`;
- страница `/profile/`;
- редактирование `/profile/edit/` (имя, email, город, о себе).

## Модель

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
```

**OneToOneField** - связь один к одному: один пользователь → один профиль. Обратная связь: `request.user.profile`.

При регистрации создаётся пустой профиль:

```python
Profile.objects.create(user=user)
```

## Проверка Part 1

1. Зарегистрируйтесь.
2. Откройте `/profile/` - username, поля профиля.
3. Откройте `/profile/edit/` - измените город и «о себе».

**Part 1 завершён?** Переходите к Part 2.

---

# Part 2 - Authorization (свои отзывы)

**Тема этой части:** кто может изменять отзыв. **Не** профиль - только ownership и CRUD для **своих** отзывов.

## Что изучаем в Part 2

- отзыв связан только с `User` (поле `author_name` удалено);
- проверка владельца: `review.user == request.user`;
- редактирование и удаление только своих отзывов.

## Authentication vs Authorization

В Lesson 09 `@login_required` отвечает только на вопрос: **вошёл ли пользователь?**

> **Напоминание:** CRUD товаров (`product_create`, `product_update`, `product_delete`) в Lesson 09-10 защищён только входом в аккаунт. Любой залогиненный пользователь может менять любой товар. Это **не баг** - каталог в курсе считается «админским» контентом. Подробнее - в README Lesson 09.

```
@login_required → пользователь вошёл? → да → view выполняется
```

**Authorization** отвечает: **может ли этот пользователь изменить этот объект?**

```
@login_required → вошёл? → да → это ЕГО отзыв? → проверяем в коде
```

`@login_required` **не** проверяет владельца. Без отдельной проверки залогиненный пользователь мог бы открыть URL редактирования чужого отзыва.

```python
if review.user != request.user:
    raise Http404
```

## Эволюция Review (кратко)

| Урок | Автор отзыва |
|------|----------------|
| 08 | `author_name` (текст) |
| 09 | `author_name` + `user` |
| 10 | только `user` → `{{ review.user.username }}` |

## Модель Review в Lesson 10

```python
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField()
```

## Проверка Part 2

1. Оставьте отзыв на товаре - появятся «Изменить» / «Удалить».
2. Войдите другим пользователем - у чужого отзыва этих ссылок нет.
3. Откройте URL редактирования чужого отзыва - 404.

## Тесты

В `shop/tests.py` - тесты ownership для отзывов и напоминание, что товары **без** проверки владельца (намеренно).

```bash
python manage.py test
```

---

## Итог урока

| Часть | Что изучили |
|-------|-------------|
| **Part 1** | профиль через OneToOneField |
| **Part 2** | authorization - только свои отзывы |

ManyToManyField (например, теги товаров) - в будущих уроках курса.

## Домашнее задание

### Part 1

Добавьте поле `phone` в Profile.

### Part 2

Не показывайте форму отзыва, если пользователь уже оставил отзыв на этот товар.

## После этого урока

Вы должны уметь:

- создать модель `Profile` с `OneToOneField` к `User`;
- показать и редактировать профиль пользователя;
- объяснить разницу между authentication и authorization;
- проверить владельца объекта (`review.user == request.user`);
- разрешить редактирование и удаление только своих отзывов.

## Следующий урок

[Lesson 11 - Cart](../11-cart/README.md) (в разработке)

## Предыдущий урок

[Lesson 09 - Authentication](../09-auth/README.md)

# Lesson 10 - Profiles (OneToOneField)

**Главная тема урока:** модель `Profile` и связь **OneToOneField** с `User`.

## Что изучается в этом уроке

- `OneToOneField`;
- модель `Profile`;
- страница `/profile/`;
- редактирование профиля через ModelForm;
- `Profile.objects.get_or_create`.

Цепочка:

```
User
    ↓
OneToOneField
    ↓
Profile
    ↓
/profile/ и /profile/edit/
```

Отзывы и права на них - в **Lesson 11**. Корзина - в **Lesson 12**.

## Запуск

```bash
py -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Что уже было в Lesson 09

- регистрация, login, logout, `request.user`;
- отзывы с полями `author_name` + `user` (переходный этап).

## Что добавляется в этом уроке

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
```

При регистрации:

```python
Profile.objects.create(user=user)
```

В views профиля используется `Profile.objects.get_or_create(user=request.user)`. Это не дублирование: при регистрации профиль уже есть, но пользователь мог быть создан через Django Admin или до появления модели `Profile` - `get_or_create` подстрахует такие случаи.

## Проверка

1. Зарегистрируйтесь.
2. Откройте `/profile/`.
3. Измените город и «о себе» на `/profile/edit/`.

## Итог урока

Профиль пользователя через OneToOneField, отдельная страница и форма редактирования.

## Домашнее задание

Добавьте поле `phone` в `Profile`.

## После этого урока

Вы должны уметь:

- объяснить OneToOneField;
- создать модель `Profile` связанную с `User`;
- показать и редактировать профиль через ModelForm;
- использовать `get_or_create` для профиля.

## Следующий урок

[Lesson 11 - Authorization](../11-authorization/README.md)

## Предыдущий урок

[Lesson 09 - Authentication](../09-auth/README.md)

# Lesson 10 - Profiles (OneToOneField)

Десятый урок курса Django for Beginners. Вы продолжите проект из Lesson 09 и добавите профиль пользователя через **OneToOneField**.

**Главная тема урока:** модель `Profile` и связь **OneToOneField** с `User`.

## Что нужно знать до урока

Модель `User`, authentication, `ModelForm` и `login_required`.

## Что не нужно запоминать

Custom User, signals и автоматическое создание профиля через сложные механизмы. Здесь достаточно обычной модели и двух view.

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

## Что уже было в Lesson 09

- регистрация, login, logout, `request.user`;
- отзывы с полями `author_name` + `user` (переходный этап).

## Что добавляется в этом уроке

### Новые и изменённые файлы

| Файл | Зачем |
|------|-------|
| `shop/models.py` | модель `Profile` |
| `shop/admin.py` | профиль в Django Admin |
| `shop/forms.py` | формы пользователя и профиля |
| `shop/views.py` | просмотр и редактирование профиля |
| `shop/urls.py` | адреса `/profile/` и `/profile/edit/` |
| `shop/templates/shop/profile.html` | страница профиля |
| `shop/templates/shop/profile_form.html` | форма редактирования |
| `shop/templates/shop/base.html` | ссылка «Профиль» в навигации |
| `shop/migrations/0004_profile.py` | таблица профилей в базе |
| `shop/tests.py` | проверки создания и доступа к профилю |

## Шаг 1. Модель Profile

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
```

`OneToOneField` означает: у одного пользователя может быть только один профиль. Через `user.profile` можно получить профиль пользователя.

- `on_delete=models.CASCADE` - при удалении пользователя удаляется его профиль;
- `related_name='profile'` - создаёт удобную обратную связь `user.profile`;
- `blank=True` - поле можно оставить пустым.

## Шаг 2. Миграция

После изменения модели создайте и примените миграцию:

```bash
python manage.py makemigrations shop
python manage.py migrate
```

В готовом уроке это файл `shop/migrations/0004_profile.py`.

## Шаг 3. Формы

В `shop/forms.py` нужны две формы:

- `UserDetailsForm` меняет `first_name` и `email` встроенной модели `User`;
- `ProfileForm` меняет `bio` и `city` модели `Profile`.

Обе формы получают существующий объект через `instance=...`. Поэтому Django обновляет запись, а не создаёт новую.

## Шаг 4. Views профиля

```python
profile_obj, _ = Profile.objects.get_or_create(user=request.user)
```

### Почему get_or_create, если профиль создаётся при регистрации?

`get_or_create` сначала ищет профиль. Если профиль не найден, Django создаёт его. Это нужно для пользователей, которых создали через Admin или до появления модели `Profile`.

View `profile` показывает данные. View `profile_edit` обрабатывает две формы в одном POST:

```python
if user_form.is_valid() and profile_form.is_valid():
    user_form.save()
    profile_form.save()
```

Обе view защищены `@login_required`.

## Шаг 5. URLs и шаблоны

```python
path('profile/', views.profile, name='profile'),
path('profile/edit/', views.profile_edit, name='profile_edit'),
```

`profile.html` показывает имя, email, город и текст «О себе». `profile_form.html` выводит обе формы и их ошибки.

В `base.html` ссылка «Профиль» показывается только вошедшему пользователю.

## Шаг 6. Профиль при регистрации

Сразу после создания пользователя:

```python
Profile.objects.create(user=user)
```

Так новый аккаунт сразу получает пустой профиль.

## Проверка

1. Зарегистрируйтесь.
2. Откройте `/profile/`.
3. Измените город и «о себе» на `/profile/edit/`.

## Тесты

```bash
python manage.py test
```

Тесты проверяют главную страницу, создание профиля при регистрации, редирект анонимного пользователя и отображение города.

## Проверь себя

1. Чем `OneToOneField` отличается от обычного ForeignKey?
2. Почему пользователь иногда может существовать без Profile?
3. Зачем `profile_edit` обрабатывает две формы?

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

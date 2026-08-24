# Lesson 09 - Authentication

Десятый урок курса Django for Beginners. Вы продолжите проект из Lesson 08 и добавите **регистрацию, вход и выход** пользователей.

## Что изучается в этом уроке

- модель User;
- registration (регистрация);
- login и logout;
- `request.user`;
- `login_required`;
- authentication vs authorization;
- `UserCreationForm`;
- `LoginView` и `LogoutView`.

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

## Что уже было в Lesson 08

В прошлом уроке вы:

- связали Product с Category;
- добавили модель Review;
- любой посетитель мог создавать товары и отзывы.

Для магазина это небезопасно: не все действия должны быть доступны всем.

## Что добавляется в этом уроке

- регистрация, вход, выход;
- `request.user` в шаблонах;
- `@login_required` на CRUD и отзывы;
- поле **`user`** в модели `Review` (ForeignKey к User).

### Переход Review: author_name → user

В Lesson 08 отзыв хранил только текст `author_name`. Теперь добавляем связь с аккаунтом:

```python
user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
```

При создании отзыва:

```python
review.user = request.user
review.author_name = request.user.get_username()  # для совместимости с демо-данными
```

В Lesson 10 поле `author_name` будет удалено - отзыв будет принадлежать только `User`.

## Authentication vs Authorization

| | Authentication | Authorization |
|---|----------------|---------------|
| Вопрос | Кто вы? | Что вам можно? |
| Пример | login / logout | только свой отзыв можно редактировать |
| В Django | `django.contrib.auth` | permissions, groups, `login_required` |

На этом уроке мы закрываем действия для **незалогиненных** пользователей. Разграничение "свой / не свой" отзыв - в Lesson 10.

## Структура проекта

```
09-auth/
├── django_shop/
│   └── settings.py     # LOGIN_URL, LOGIN_REDIRECT_URL
└── shop/
    ├── forms.py        # RegisterForm
    ├── views.py        # register + login_required
    ├── urls.py         # accounts/login, logout, register
    └── templates/shop/
        ├── login.html
        └── register.html
```

## Шаг 1. Настройки в settings.py

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

- `LOGIN_URL` - куда перенаправить незалогиненного пользователя;
- `LOGIN_REDIRECT_URL` - куда идти после успешного входа;
- `LOGOUT_REDIRECT_URL` - после выхода.

`django.contrib.auth` и `AuthenticationMiddleware` уже были в проекте с Lesson 00.

## Шаг 2. Форма регистрации

`shop/forms.py`:

```python
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)
```

`UserCreationForm` - готовая форма Django с полями username, password1, password2 и валидацией пароля.

## Шаг 3. View register

```python
from django.contrib.auth import login
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to Django Shop!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})
```

`form.save()` создает записи User в базе. `login(request, user)` авторизует пользователя сразу после регистрации.

## Шаг 4. Login и Logout

В `shop/urls.py`:

```python
from django.contrib.auth import views as auth_views

path('accounts/register/', views.register, name='register'),
path(
    'accounts/login/',
    auth_views.LoginView.as_view(template_name='shop/login.html'),
    name='login',
),
path(
    'accounts/logout/',
    auth_views.LogoutView.as_view(),
    name='logout',
),
```

`LoginView` - встроенный class-based view для входа. Шаблон `login.html` с полями username и password.

Logout в Django 5 отправляется через **POST** (безопасность):

```html
<form method="post" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit">Logout</button>
</form>
```

## Шаг 5. request.user в шаблоне

В `base.html` доступен объект `user` (через `auth` context processor):

```html
{% if user.is_authenticated %}
    <span>Hi, {{ user.username }}</span>
    ...
{% else %}
    <a href="{% url 'login' %}">Login</a>
    <a href="{% url 'register' %}">Register</a>
{% endif %}
```

`request.user` в view - тот же пользователь. Если не залогинен - `AnonymousUser`.

## Шаг 6. login_required

Защитите views, которые должны быть только для авторизованных:

```python
from django.contrib.auth.decorators import login_required


@login_required
def product_create(request):
    ...


@login_required
def review_create(request, pk):
    ...
```

Если незалогиненный пользователь откроет `/products/create/`, Django перенаправит на `/accounts/login/`.

Декоратор `@login_required` можно ставить на:

- `product_create`, `product_update`, `product_delete`;
- `review_create`.

## Товары vs отзывы: это не баг

`product_create`, `product_update` и `product_delete` защищены только `@login_required`. **Любой** залогиненный пользователь может изменить любой товар - в отличие от отзывов в Lesson 10, где проверяется владелец.

Это **намеренно** для курса:

| Объект | Защита в Lesson 09 | Почему |
|--------|-------------------|--------|
| Товар | только `login_required` | каталог - «админский» контент; в реальном проекте товары обычно меняют через `/admin/` или staff permissions |
| Отзыв | `login_required` + владелец (Lesson 10) | там мы изучаем **authorization** |

`@login_required` отвечает: «вошёл ли пользователь?» Он **не** отвечает: «может ли этот пользователь менять этот товар?»

В Lesson 16 и в реальных проектах для каталога используют Django Admin, группы (`is_staff`) или отдельные permissions - не открывают CRUD товаров для всех зарегистрированных.

## Шаг 7. Отзывы от текущего пользователя

В `review_create`:

```python
review.author_name = request.user.get_username()
```

Поле `author_name` в форме убрано - имя берется из аккаунта.

В шаблоне форма отзыва показывается только если `user.is_authenticated`.

## Шаг 8. Проверка и запуск

```bash
python manage.py migrate
python manage.py runserver
```

Тестовые данные: через Admin или см. [Test data](../../TEST_DATA.md).

Проверьте сценарии:

| Действие | Ожидание |
|----------|----------|
| Открыть `/products/create/` без входа | Редирект на login |
| Register | Новый пользователь, вход выполнен |
| Login / Logout | Сессия создается и завершается |
| Добавить отзыв без входа | Ссылка "Log in to leave a review" |
| Добавить отзыв после входа | Отзыв с вашим username |

## Тесты (введение)

В `shop/tests.py` - простые тесты: редирект на login и валидация `rating` в модели.

```bash
python manage.py test
```

Тесты не обязательны для прохождения курса, но показывают, как Django проверяет код автоматически. В ранних уроках `tests.py` пустой - это нормально.

## Итог урока

Вы добавили систему аутентификации: регистрация, вход, выход, `request.user` и защита views через `login_required`. Магазин перестал быть полностью открытым для изменений.

## Домашнее задание

1. После logout перенаправьте на страницу login вместо home (измените `LOGOUT_REDIRECT_URL`).
2. Скройте кнопки Edit/Delete на странице товара для незалогиненных (уже в шаблоне - проверьте).
3. Добавьте на страницу register текст с объяснением правил пароля Django.

## После этого урока

Вы должны уметь:

- объяснить разницу между authentication и authorization;
- зарегистрировать пользователя через `UserCreationForm`;
- настроить login и logout;
- использовать `request.user` и `user.is_authenticated` в шаблонах;
- защитить view декоратором `login_required`;
- настроить `LOGIN_URL` и `LOGIN_REDIRECT_URL`.

## Следующий урок

[Lesson 10 - Profiles & Authorization (OneToOneField, ownership)](../10-profiles-reviews/README.md)

## Предыдущий урок

[Lesson 08 - ForeignKey](../08-foreign-key/README.md)

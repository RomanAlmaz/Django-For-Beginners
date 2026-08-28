# Lesson 09 - Authentication

Девятый урок курса Django for Beginners. Вы продолжите проект из Lesson 08 и добавите **регистрацию, вход и выход** пользователей.

## Что нужно знать до урока

Формы, POST, redirect, модели и ForeignKey.

## Что не нужно запоминать

Как Django хеширует пароли и хранит session внутри. Используйте готовые `UserCreationForm`, `LoginView` и `LogoutView`.

## Что изучается в этом уроке

- модель User;
- registration (регистрация);
- login и logout;
- `request.user`;
- `@login_required`;
- `UserCreationForm`;
- `LoginView` и `LogoutView`.

Разница authentication / authorization - коротко; ownership и permissions - в **Lesson 11**.

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
review = form.save(commit=False)
review.product = product
review.user = request.user
review.author_name = request.user.get_username()  # для совместимости с демо-данными
review.save()
```

Как и в Lesson 08, `commit=False` создаёт объект в памяти. Перед сохранением сервер сам добавляет товар и текущего пользователя.

В Lesson 11 поле `author_name` будет удалено - отзыв будет принадлежать только `User`.

## Authentication и Authorization (кратко)

| | Authentication | Authorization |
|---|----------------|---------------|
| Вопрос | Кто вы? | Что вам разрешено? |
| Пример | login / logout | только **свой** отзыв можно редактировать |

На **этом** уроке мы закрываем действия для **незалогиненных** пользователей. Проверка «свой / не свой» объект - в **Lesson 11**.

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
        labels = {
            'username': 'Имя пользователя',
            'email': 'Почта',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].help_text = 'Обязательное поле. До 150 символов.'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password1'].help_text = (
            'Минимум 8 символов. Пароль не должен быть слишком простым.'
        )
        self.fields['password2'].help_text = 'Повторите пароль для проверки.'
```

`UserCreationForm` - готовая форма Django с полями username, password1, password2 и валидацией пароля. В `__init__` мы меняем только подписи и подсказки, логика проверки остаётся стандартной.

## Шаг 3. View register

Сокращённая версия с основной логикой:

```python
from django.contrib.auth import login
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Добро пожаловать в Django Shop!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})
```

`form.save()` создаёт запись User в базе. `login(request, user)` авторизует пользователя сразу после регистрации.

`messages.success()` сохраняет короткое сообщение до следующей страницы. После redirect его показывает `base.html`:

```django
{% if messages %}
    <ul class="messages">
        {% for message in messages %}
            <li class="message {{ message.tags }}">{{ message }}</li>
        {% endfor %}
    </ul>
{% endif %}
```

Это небольшой готовый механизм Django. Достаточно понимать: view создаёт сообщение, а базовый шаблон показывает его один раз.

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
    <button type="submit">Выход</button>
</form>
```

## Шаг 5. request.user в шаблоне

В `base.html` доступен объект `user` (через `auth` context processor):

```html
{% if user.is_authenticated %}
    <span class="nav-user">Привет, {{ user.username }}</span>
    <form method="post" action="{% url 'logout' %}" class="logout-form">
        {% csrf_token %}
        <button type="submit" class="link-button">Выход</button>
    </form>
{% else %}
    <a href="{% url 'login' %}">Вход</a>
    <a href="{% url 'register' %}">Регистрация</a>
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

## Важно: CRUD товаров специально упрощён

`product_create`, `product_update` и `product_delete` защищены только `@login_required`. **Любой** залогиненный пользователь может изменить любой товар - в отличие от отзывов в Lesson 11, где проверяется владелец.

> Это только учебное упрощение. В реальном магазине обычный пользователь не должен создавать, редактировать и удалять товары.

```text
Обычный User
    профиль, отзывы, корзина, заказы

Staff / Admin
    управление каталогом товаров
```

Сравнение:

| Объект | Защита в Lesson 09 | Почему |
|--------|-------------------|--------|
| Товар | только `login_required` | каталог - «админский» контент; в реальном проекте товары обычно меняют через `/admin/` или staff permissions |
| Отзыв | `login_required` + владелец (Lesson 11) | там мы изучаем **authorization** |

`@login_required` отвечает: «вошёл ли пользователь?» Он **не** отвечает: «может ли этот пользователь менять этот товар?»

В реальных проектах для каталога используют Django Admin, `is_staff`, группы или отдельные permissions.

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
| Добавить отзыв без входа | Ссылка «Войдите, чтобы оставить отзыв» |
| Добавить отзыв после входа | Отзыв с вашим именем пользователя |

## Тесты (введение)

Django находит методы, имя которых начинается с `test_`, запускает их и сообщает: тест прошёл или упал.

```text
test_...
    выполнить код
    проверить assert
    OK или FAILED
```

Минимальный тест страницы:

```python
class HomePageTests(TestCase):
    def test_home_page(self):
        response = Client().get(reverse('home'))
        self.assertEqual(response.status_code, 200)
```

В `shop/tests.py` также есть проверки регистрации, редиректа на login и валидации `rating`.

```bash
python manage.py test
```

Тесты не обязательны для прохождения курса, но показывают, как Django проверяет код автоматически. В ранних уроках `tests.py` пустой - это нормально.

## Проверь себя

1. Чем authentication отличается от authorization?
2. Что находится в `request.user` до и после входа?
3. Что проверяет `@login_required`, а что он не проверяет?

## Итог урока

Вы добавили систему аутентификации: регистрация, вход, выход, `request.user` и защита views через `login_required`. Магазин перестал быть полностью открытым для изменений.

## Домашнее задание

1. После logout перенаправьте на страницу login вместо home (измените `LOGOUT_REDIRECT_URL`).
2. На странице `/contact/` покажите имя пользователя, если он вошёл (`user.is_authenticated`).
3. Над формой регистрации (не в `help_text` полей) добавьте абзац своими словами: какие пароли Django считает слабыми.

## После этого урока

Вы должны уметь:

- зарегистрировать пользователя через `UserCreationForm`;
- настроить login и logout;
- использовать `request.user` и `user.is_authenticated` в шаблонах;
- защитить view декоратором `login_required`;
- настроить `LOGIN_URL` и `LOGIN_REDIRECT_URL`;
- коротко объяснить, что `login_required` - не то же самое, что проверка владельца объекта.

## Следующий урок

[Lesson 10 - Profiles (OneToOneField)](../10-profiles/README.md)

## Предыдущий урок

[Lesson 08 - ForeignKey](../08-foreign-key/README.md)

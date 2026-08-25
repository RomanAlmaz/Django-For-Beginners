# Django for Beginners

Открытый образовательный репозиторий для изучения Django. Шаг за шагом вы построите учебный интернет-магазин **Django Shop**.

**Автор:** Roman ([RomanAlmaz](https://github.com/RomanAlmaz) на GitHub)

**Репозиторий:** [github.com/RomanAlmaz/Django-For-Beginners](https://github.com/RomanAlmaz/Django-For-Beginners)

## Кому подходит этот курс

Курс для людей, которые **уже знают базовый Python**, но **никогда не работали с Django**.

**Beginner** здесь означает: новичок **в Django**, а не человек, который впервые видел Python вчера.

Если Django уже знаете - курс поможет как последовательный учебный проект.

## Требования

Перед началом желательно знать:

- **базовый Python** (функции, классы, словари, импорты);
- **основы HTML** (теги, атрибуты, формы);
- **базовый CSS** (селекторы, отступы, цвета).

**Предварительно знать Django не требуется.**

## Что такое Django

Django - Python-фреймворк для веб-разработки. Он дает готовые инструменты для URL routing, форм, админ-панели, работы с базой данных и безопасности.

## Что вы построите

В финале курса у вас будет **небольшой** учебный интернет-магазин: каталог, корзина, заказы, регистрация, отзывы. Отдельные уроки позже добавят API и базовый production deploy - **по одной теме на урок**, не всё вместе.

Главная ценность курса:

> **Я научу тебя Django постепенно** - один урок, одна основная концепция.

Не «засунуть 17 технологий за 16 уроков», а дать ученику каждый день понимать: *«Сегодня я изучаю вот эту штуку»*.

| Урок | Одна главная тема |
|------|-------------------|
| 05 | Models |
| 06 | Admin |
| 07 | CRUD |
| 08 | ForeignKey |
| 09 | Authentication |
| 10 | Profiles (OneToOneField) |
| 11 | Authorization (ownership) |
| 12 | Cart (sessions) |

Уроки 13-17 (в разработке): Orders, Pagination, Images, REST API, Production - **каждый отдельно**.

**Каждый урок - отдельный рабочий проект.** Откройте папку в `lessons/`, `migrate`, `runserver`.

## Roadmap

```
0. Hello Django          - пустой проект и ракета Django
1. First View            - первая страница
2. URLs                  - несколько страниц и URL routing
3. Templates             - HTML-шаблоны
4. Static Files          - CSS и {% static %}
5. Models                - Category, Product, миграции, ORM
6. Admin                 - Django Admin
7. CRUD                  - Create, Read, Update, Delete
8. ForeignKey            - связь Product → Category, Review
9. Authentication        - регистрация, login, logout
10. Profiles             - OneToOneField, profile page
11. Authorization        - ownership, свои отзывы
12. Cart                 - корзина через sessions

🚧 Lessons 13-17 - в разработке:
13. Orders               - заказы
14. Pagination           - постраничный список
15. Images               - загрузка изображений
16. REST API             - Django REST Framework
17. Production           - deploy, SECRET_KEY через .env
```

## Структура репозитория

```
django-for-beginners/
├── README.md
├── TEST_DATA.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
├── CURSOR_INSTRUCTIONS.txt
└── lessons/
    ├── 00-hello-django/
    ├── 01-first-app/
    └── ...
```

Каждая папка в `lessons/` - **отдельный рабочий проект** на этом этапе курса. Откройте урок и запустите его независимо.

## Как начать

```bash
git clone https://github.com/RomanAlmaz/Django-For-Beginners.git
cd Django-For-Beginners/lessons/00-hello-django
```

1. Создайте virtual environment и установите зависимости (подробности в README урока 00).
2. Выполните `python manage.py migrate`.
3. Запустите `python manage.py runserver`.

**Важно:** файл `db.sqlite3` не хранится в репозитории. База создается локально после `migrate`.

## Test data (тестовые данные)

Основной путь в курсе: **Models → migrate → Admin → создаём данные вручную**.

Команда `loaddata` и fixtures - **опционально**, для быстрой загрузки готовых категорий и товаров. Подробности в [TEST_DATA.md](TEST_DATA.md).

## Рекомендуемое окружение

| | |
|---|---|
| Python | 3.10+ (автор Roman использует **3.14**) |
| Django | **5.2.12** (в `requirements.txt` каждого урока) |
| Терминал | Git Bash на Windows (рекомендуется) |
| Git | для клонирования репозитория |

Подойдет Python 3.10+. Курс разработан и проверен на Django **5.2.12**.

Файл `tests.py` в уроках 00-08 - стандартный шаблон Django. Тестирование появится в отдельной теме; в уроках 09+ есть простые примеры тестов.

## Настройка окружения (один раз)

```bash
py -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
```

## Уроки

| Урок | Тема | Папка |
|------|------|-------|
| 00 | Hello Django | [lessons/00-hello-django](lessons/00-hello-django/) |
| 01 | First View | [lessons/01-first-app](lessons/01-first-app/) |
| 02 | URLs | [lessons/02-urls](lessons/02-urls/) |
| 03 | Templates | [lessons/03-templates](lessons/03-templates/) |
| 04 | Static Files | [lessons/04-static](lessons/04-static/) |
| 05 | Models | [lessons/05-models](lessons/05-models/) |
| 06 | Django Admin | [lessons/06-admin](lessons/06-admin/) |
| 07 | CRUD | [lessons/07-crud](lessons/07-crud/) |
| 08 | ForeignKey | [lessons/08-foreign-key](lessons/08-foreign-key/) |
| 09 | Authentication | [lessons/09-auth](lessons/09-auth/) |
| 10 | Profiles (OneToOneField) | [lessons/10-profiles](lessons/10-profiles/) |
| 11 | Authorization (ownership) | [lessons/11-authorization](lessons/11-authorization/) |
| 12 | Cart (sessions) | [lessons/12-cart](lessons/12-cart/) |

## Итоговый проект

**Django Shop** - учебный магазин, который растет с каждым уроком. Цель не production e-commerce, а понятное и последовательное изучение Django.

## Contributing

Проект открыт для исправлений, предложений и новых уроков. Как внести изменения через fork и pull request - см. [CONTRIBUTING.md](CONTRIBUTING.md).

## Лицензия

MIT License - см. [LICENSE](LICENSE).

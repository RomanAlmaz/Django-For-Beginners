# Django for Beginners

Открытый образовательный репозиторий для изучения Django. Шаг за шагом вы построите учебный интернет-магазин **Django Shop**.

**Автор:** Roman ([RomanAlmaz](https://github.com/RomanAlmaz) на GitHub)

**Репозиторий:** [github.com/RomanAlmaz/Django-For-Beginners](https://github.com/RomanAlmaz/Django-For-Beginners)

## Кому подходит этот курс

Курс для людей, которые **уже знают базовый Python**, но **никогда не работали с Django**.

**Beginner** здесь означает: новичок **в Django**, а не человек, который впервые видел Python вчера.

Если Django уже знаете - курс поможет как последовательный учебный проект.

## Требования

Перед Django желательно уметь:

**Python**

- писать функции и вызывать методы;
- использовать `if`, `for`, списки и словари;
- работать с импортами и классами;
- понимать обычный `try` / `except`.

**HTML и CSS**

- читать базовые HTML-теги, атрибуты и формы;
- понимать простые CSS-селекторы, цвета и отступы.

До курса не нужны:

- Django;
- SQL и глубокое знание HTTP;
- JavaScript и CSS-фреймворки;
- Docker, Linux, Redis и другие production-инструменты.

## Что такое Django

Django - Python-фреймворк для веб-разработки. Он дает готовые инструменты для URL routing, форм, админ-панели, работы с базой данных и безопасности.

## Почему Django стоит изучать

Django позволяет сосредоточиться на логике сайта, а не писать с нуля вход пользователей, работу с базой и защиту форм. У него подробная документация, большое сообщество и понятная структура проекта.

## Что вы построите

В финале курса у вас будет **небольшой** учебный интернет-магазин: каталог, корзина, заказы, регистрация, отзывы. Отдельные уроки позже добавят API и базовый production deploy - **по одной теме на урок**, не всё вместе.

Главная ценность курса:

> **Я научу тебя Django постепенно** - один урок, одна основная концепция.

Не «засунуть 17 технологий за 16 уроков», а дать ученику каждый день понимать: *«Сегодня я изучаю вот эту штуку»*.

| Урок | Одна главная тема |
|------|-------------------|
| 00 | Hello Django |
| 01 | First View |
| 02 | URLs |
| 03 | Templates |
| 04 | Static Files |
| 05 | Models |
| 06 | Admin |
| 07 | CRUD |
| 08 | ForeignKey |
| 09 | Authentication |
| 10 | Profiles (OneToOneField) |
| 11 | Authorization (ownership) |
| 12 | Cart (sessions) |
| 13 | Orders |

Уроки 14-17 (в разработке): Pagination, Images, REST API, Production - **каждый отдельно**.

**Каждый урок - отдельный рабочий проект.** Откройте папку в `lessons/`, `migrate`, `runserver`.

## Уровень сложности

- **Lessons 00-10** - основы Django: project, views, templates, models, forms и authentication.
- **Lessons 11-13** - переход к реальному backend-коду: права на объекты, session-корзина и транзакции.

Во второй части нормально возвращаться к предыдущим урокам. Не нужно запоминать все механизмы с первого раза.

Lesson 13 завершает первый цельный курс. Pagination, search, API и production-настройки относятся к следующему уровню и не должны усложнять первые 14 уроков.

Интерфейс тоже развивается постепенно: Lesson 04 добавляет базовые стили, Lesson 07 оформляет формы, а Lessons 11-13 переходят к более цельной responsive-вёрстке. Поэтому ранние уроки намеренно выглядят проще поздних.

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
13. Orders               - Order, OrderItem, checkout, transaction.atomic()

🚧 Lessons 14-17 - в разработке:
14. Pagination           - постраничный список
15. Images               - загрузка изображений
16. REST API             - Django REST Framework
17. Production           - deploy, SECRET_KEY через .env
```

## Структура репозитория

```
Django-For-Beginners/
├── README.md
├── TEST_DATA.md
├── TROUBLESHOOTING.md
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

> **Важно:** каждый урок - снимок проекта на конкретном этапе. Работайте только в папке выбранного урока и не переносите файлы между уроками вручную. Изменения, сделанные вами в Lesson 08, не появятся автоматически в Lesson 09: Lesson 09 уже содержит готовый снимок следующего этапа.

## Как начать

```bash
git clone https://github.com/RomanAlmaz/Django-For-Beginners.git
cd Django-For-Beginners/lessons/00-hello-django
```

1. Создайте virtual environment и установите зависимости (подробности в README урока 00).
2. Выполните `python manage.py migrate`.
3. Запустите `python manage.py runserver`.

**Важно:** файл `db.sqlite3` не хранится в репозитории. База создается локально после `migrate`.

Если команда или страница не работает, откройте [решение частых проблем](TROUBLESHOOTING.md).

## Test data (тестовые данные)

Основной путь в курсе: **Models → migrate → Admin → создаём данные вручную**.

Команда `loaddata` и fixtures - **опционально**, для быстрой загрузки готовых категорий и товаров. Подробности в [TEST_DATA.md](TEST_DATA.md).

## Рекомендуемое окружение

| | |
|---|---|
| Python | **3.14.x** (рекомендуется; автор Roman проверял курс на **3.14.3**) |
| Django | **5.2.12** (в `requirements.txt` каждого урока) |
| Терминал | Command Prompt, PowerShell или Git Bash на Windows |
| Git | для клонирования репозитория |

Рекомендуется **Python 3.14.x**. Python 3.10-3.14 теоретически поддерживаются Django 5.2, но автор курса тестировал курс на **Python 3.14.3** и **Django 5.2.12**. Остальные версии диапазона отдельно в этом репозитории не тестируются.

В Lessons 02-04 `tests.py` остаётся пустым шаблоном `startapp`. В Lessons 05-08 появляется по одному простому тесту для знакомства. С Lesson 09 тесты начинают проверять основные пользовательские сценарии.

## Настройка окружения для выбранного урока

Сначала перейдите в папку нужного урока. Если virtual environment уже создан, повторно создавать его не нужно.

**Windows (Command Prompt):**

```bat
py -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
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
| 13 | Orders | [lessons/13-orders](lessons/13-orders/) |

## Итоговый проект

**Django Shop** - учебный магазин, который растет с каждым уроком. Цель не production e-commerce, а понятное и последовательное изучение Django.

## Contributing

Проект открыт для исправлений, предложений и новых уроков. Как внести изменения через fork и pull request - см. [CONTRIBUTING.md](CONTRIBUTING.md).

## Лицензия

MIT License - см. [LICENSE](LICENSE).

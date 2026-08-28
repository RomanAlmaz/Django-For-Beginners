# Lesson 13 - Orders (заказы)

Тринадцатый урок курса Django for Beginners. Вы продолжите проект из Lesson 12 и научитесь сохранять **заказы** в базе данных.

**Главная тема урока:** сохранение заказа в **базе данных** и оформление из корзины.

## Что нужно знать до урока

Модели, ForeignKey, формы, ownership и session-корзину из Lesson 12.

## Что не нужно запоминать

Проектирование платёжных систем, защиту от одновременных запросов и сложные транзакции. Достаточно понять: заказ и позиции сохраняются вместе.

## Что изучается в этом уроке

- модели `Order` и `OrderItem`;
- checkout (оформление заказа);
- статус заказа (`status` + choices);
- `transaction.atomic()` - все записи создаются вместе или не создаются вообще;
- очистка корзины после успешного заказа;
- ownership заказа (видеть может только владелец).

## Цель урока

**Главное:** превратить уже знакомую корзину в `Order` и несколько `OrderItem`, а затем сохранить их вместе.

Sessions, POST, CSRF, ForeignKey, ownership и `Decimal` уже встречались раньше. Здесь мы используем их повторно, а не изучаем заново.

Цепочка:

```
Корзина (session)
    ↓
/checkout/ → POST
    ↓
Order + OrderItem (БД)
    ↓
clear_cart()
    ↓
/orders/<id>/
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

`DEBUG=True` и учебный `SECRET_KEY` подходят только для локальной разработки. Production-настройки будут отдельной темой в Lesson 17.

## Что уже было в Lesson 12

- корзина в `request.session`;
- модуль `shop/cart.py`;
- страница `/cart/`.

## Что добавляется в этом уроке

### Модели

```python
class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_PAID = 'paid'
    ...
    user = models.ForeignKey(User, ...)
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_NEW)
    total = models.DecimalField(...)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', ...)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(...)  # снимок названия
    price = models.DecimalField(...)      # снимок цены
    quantity = models.PositiveSmallIntegerField(...)
```

`product_name` и `price` сохраняются **на момент заказа**. Если цена товара потом изменится, в старом заказе останется прежняя сумма.

Зачем хранить и `product`, и копии данных:

```text
product
    ссылка на текущий товар

product_name + price
    история товара в момент покупки
```

Пример:

```text
2026: Product «Книга» стоит 100 руб.
      OrderItem сохраняет «Книга», 100 руб.

2027: Product «Книга» стоит 150 руб.
      Старый OrderItem всё ещё показывает 100 руб.
```

Связь `product` позволяет открыть актуальную страницу товара. Поля `product_name` и `price` не дают изменению товара переписать историю заказа.

У `Order.total` стоит `max_digits=14`, потому что сумма нескольких товаров может быть больше цены одного `Product`.

`on_delete=models.PROTECT` на `OrderItem.product` запрещает удалить товар из базы, если он уже есть в заказе. View `product_delete` проверяет `product.order_items.exists()` и показывает сообщение, а не страницу ошибки. На странице товара ссылка **Удалить** скрыта, если товар уже есть в заказе.

`Order.user` использует `on_delete=models.CASCADE`: при удалении пользователя его заказы тоже удалятся. Для учебного проекта это проще. В реальном магазине заказ часто сохраняют, а данные пользователя анонимизируют по отдельным правилам.

### Новые и изменённые файлы

| Файл | Зачем |
|------|--------|
| `shop/models.py` | модели `Order` и `OrderItem` |
| `shop/views.py` | checkout и страницы заказов |
| `shop/urls.py` | адреса checkout и заказов |
| `shop/orders.py` | создание заказа из корзины |
| `shop/migrations/0006_order_orderitem.py` | таблицы `Order` и `OrderItem` |
| `shop/templates/shop/checkout.html` | подтверждение заказа |
| `shop/templates/shop/order_list.html` | список своих заказов |
| `shop/templates/shop/order_detail.html` | один заказ |
| `shop/templates/shop/cart.html` | ссылка «Оформить заказ» |
| `shop/templates/shop/base.html` | ссылка «Заказы» |
| `shop/templates/shop/product_detail.html` | запрет удаления товара из заказа |
| `shop/admin.py` | просмотр заказа и изменение статуса |
| `shop/static/shop/css/style.css` | стили checkout и заказов |
| `shop/tests.py` | проверки заказов и регрессии корзины |

Миграция `0006_order_orderitem.py` создаёт обе таблицы заказа.

### transaction.atomic()

Представим ошибку на третьей позиции:

```text
Создали Order          OK
Создали OrderItem 1    OK
Создали OrderItem 2    OK
Создали OrderItem 3    ERROR
```

Без транзакции в базе останется незавершённый заказ с двумя позициями. С `transaction.atomic()` Django откатит `Order` и обе созданные позиции.

```python
with transaction.atomic():
    order = Order.objects.create(...)
    for line in lines:
        OrderItem.objects.create(...)

clear_cart(session)
```

Если при создании позиций произойдёт ошибка, Django **откатит** заказ и позиции в базе. Код не дойдёт до `clear_cart`, поэтому корзина останется.

Важно: `transaction.atomic()` управляет только **базой данных**, а session живёт отдельно. Поэтому `clear_cart` вызывается после блока `transaction.atomic()`, когда транзакция уже успешно завершилась.

Логика вынесена в `shop/orders.py` (как `cart.py` для корзины).

Функция `create_order_from_cart(user, session)` получает `user` и `session`, а не весь `request`. Мы специально передаём только те данные, которые функции реально нужны. `orders.py` не должен знать о полном HTTP request.

Если POST на `/checkout/` пришёл с уже пустой корзиной (двойной клик, вторая вкладка), заказ не создаётся: редирект обратно на `/cart/`.

### URLs

| URL | Назначение |
|-----|------------|
| `/checkout/` | просмотр и подтверждение заказа |
| `/orders/` | список своих заказов |
| `/orders/<id>/` | детали заказа |

Оформление заказа доступно только **вошедшим** пользователям (`@login_required`).

В Django Admin нельзя вручную создать или удалить заказ. Пользователь, сумма и позиции доступны только для чтения, менять можно статус. Это защищает историю заказа от случайного изменения.

Чтобы открыть Admin в новом проекте урока, сначала создайте администратора:

```bash
python manage.py createsuperuser
```

## Проверка

1. Войдите в аккаунт.
2. Добавьте товары в корзину.
3. На `/cart/` нажмите **Оформить заказ**.
4. На `/checkout/` нажмите **Подтвердить заказ**.
5. Откройте `/orders/` - заказ в списке, корзина пуста.
6. В Django Admin измените статус заказа на «Оплачен».

| Действие | Ожидание |
|----------|----------|
| `/checkout/` без входа | редирект на login |
| `/checkout/` с пустой корзиной (GET или POST) | редирект на `/cart/` |
| POST checkout | заказ в БД, корзина очищена |
| чужой `/orders/<id>/` | 404 |
| удалить товар, который уже в заказе | товар остаётся, сообщение об ошибке |

## Тесты

```bash
python manage.py test
```

Тесты корзины из Lesson 12 сохранены как регрессионные (повторные) проверки: новый код заказов не должен ломать уже изученную функциональность.

Отдельный тест фиксирует снимок цены: товар стоит 100, после заказа цена становится 150, в `OrderItem` остаётся 100.

## Проверь себя

1. Почему заказ разделён на `Order` и `OrderItem`?
2. Что гарантирует `transaction.atomic()`?
3. Чем `product` отличается от `product_name` и `price` в позиции заказа?
4. Почему корзина очищается только после успешной транзакции?

## Итог урока

Заказ сохраняется в базе: `Order`, `OrderItem`, checkout, статус, транзакция, очистка корзины.

## Домашнее задание

1. На странице профиля покажите последние 3 заказа пользователя.
2. На странице заказа, если статус «Новый», покажите текст, что оплата ещё не прошла.

## После этого урока

Вы должны уметь:

- создать модели заказа и позиций заказа;
- оформить заказ из данных session-корзины;
- использовать `transaction.atomic()` для связанных записей;
- сохранить снимок цены и названия товара;
- ограничить доступ к заказу владельцу;
- понять, зачем `PROTECT` на товаре в заказе.

## Следующий урок

Lesson 14 - Pagination пока в разработке, поэтому ссылки на папку ещё нет.

## Предыдущий урок

[Lesson 12 - Cart](../12-cart/README.md)

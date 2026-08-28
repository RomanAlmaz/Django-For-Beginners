from django.db import transaction

from shop.cart import clear_cart, get_cart_lines
from shop.models import Order, OrderItem


def create_order_from_cart(user, session):
    """
    Создаёт заказ из корзины в session и очищает корзину.
    Возвращает Order или None, если корзина пуста.
    """
    lines, total = get_cart_lines(session)
    if not lines:
        return None

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            total=total,
            status=Order.STATUS_NEW,
        )
        for line in lines:
            OrderItem.objects.create(
                order=order,
                product=line['product'],
                product_name=line['product'].name,
                price=line['product'].price,
                quantity=line['quantity'],
            )

    # Транзакция БД уже успешно завершилась. Только теперь очищаем session.
    clear_cart(session)
    return order

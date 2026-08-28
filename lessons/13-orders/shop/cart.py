"""Корзина хранится в session как {'product_id': quantity}."""

from decimal import Decimal

from shop.models import Product

CART_SESSION_KEY = 'cart'
MAX_CART_QUANTITY = 99


def _get_cart(session):
    return session.get(CART_SESSION_KEY, {})


def _save_cart(session, cart):
    session[CART_SESSION_KEY] = cart
    session.modified = True


def _to_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def add_to_cart(session, product_id, quantity=1):
    if not Product.objects.filter(pk=product_id).exists():
        return

    cart = _get_cart(session)
    product_key = str(product_id)

    quantity = _to_int(quantity, 1)
    quantity = max(1, min(quantity, MAX_CART_QUANTITY))

    current_quantity = cart.get(product_key, 0)
    cart[product_key] = min(
        current_quantity + quantity,
        MAX_CART_QUANTITY,
    )
    _save_cart(session, cart)


def update_cart_item(session, product_id, quantity):
    cart = _get_cart(session)
    product_key = str(product_id)
    quantity = _to_int(quantity, 0)

    if quantity <= 0:
        cart.pop(product_key, None)
    else:
        cart[product_key] = min(quantity, MAX_CART_QUANTITY)

    _save_cart(session, cart)


def remove_from_cart(session, product_id):
    cart = _get_cart(session)
    cart.pop(str(product_id), None)
    _save_cart(session, cart)


def clear_cart(session):
    _save_cart(session, {})


def get_cart_lines(session):
    cart = _get_cart(session)
    if not cart:
        return [], Decimal('0.00')

    lines = []
    total = Decimal('0.00')
    stale_keys = []
    parsed_items = []

    for product_key, quantity in cart.items():
        try:
            product_id = int(product_key)
        except (TypeError, ValueError):
            stale_keys.append(product_key)
            continue
        parsed_items.append((product_key, product_id, quantity))

    products = Product.objects.in_bulk(
        [product_id for _, product_id, _ in parsed_items]
    )

    for product_key, product_id, quantity in parsed_items:
        product = products.get(product_id)
        if product is None:
            stale_keys.append(product_key)
            continue

        line_total = product.price * quantity
        lines.append({
            'product': product,
            'quantity': quantity,
            'line_total': line_total,
        })
        total += line_total

    if stale_keys:
        for product_key in stale_keys:
            del cart[product_key]
        _save_cart(session, cart)

    return lines, total


def get_cart_item_count(session):
    lines, _ = get_cart_lines(session)
    return sum(line['quantity'] for line in lines)


def is_product_in_cart(session, product_id):
    lines, _ = get_cart_lines(session)
    return any(line['product'].pk == product_id for line in lines)

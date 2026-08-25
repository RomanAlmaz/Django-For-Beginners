from decimal import Decimal

from shop.models import Product

CART_SESSION_KEY = 'cart'
MAX_CART_QUANTITY = 99


def _get_cart_dict(session):
    cart = session.get(CART_SESSION_KEY, {})
    if not isinstance(cart, dict):
        cart = {}
    return cart


def _normalize_for_add(quantity):
    """Добавление: некорректное или отрицательное количество → 1."""
    try:
        qty = int(quantity)
    except (TypeError, ValueError):
        qty = 1
    if qty < 1:
        qty = 1
    if qty > MAX_CART_QUANTITY:
        qty = MAX_CART_QUANTITY
    return qty


def _parse_update_quantity(quantity):
    """Изменение: <= 0 → удалить позицию; 1..99 → установить; > 99 → 99."""
    try:
        qty = int(quantity)
    except (TypeError, ValueError):
        qty = 0
    if qty > MAX_CART_QUANTITY:
        qty = MAX_CART_QUANTITY
    return qty


def _clamp_stored_quantity(quantity):
    """Нормализация значения уже сохранённого в session (очистка повреждённых данных)."""
    try:
        qty = int(quantity)
    except (TypeError, ValueError):
        qty = 1
    if qty < 1:
        qty = 1
    if qty > MAX_CART_QUANTITY:
        qty = MAX_CART_QUANTITY
    return qty


def _parse_cart_key(key):
    try:
        return int(key)
    except (TypeError, ValueError):
        return None


def _sync_cart_with_products(session):
    cart = _get_cart_dict(session)
    if not cart:
        return cart

    parsed_entries = []
    for key, value in cart.items():
        product_id = _parse_cart_key(key)
        if product_id is None:
            continue
        parsed_entries.append((product_id, str(product_id), value))

    if not parsed_entries:
        session[CART_SESSION_KEY] = {}
        session.modified = True
        return {}

    product_ids = [entry[0] for entry in parsed_entries]
    existing_ids = set(
        Product.objects.filter(pk__in=product_ids).values_list('pk', flat=True)
    )
    cleaned = {
        key: _clamp_stored_quantity(value)
        for product_id, key, value in parsed_entries
        if product_id in existing_ids
    }
    if cleaned != cart:
        session[CART_SESSION_KEY] = cleaned
        session.modified = True
    return cleaned


def is_product_in_cart(session, product_id):
    cart = _sync_cart_with_products(session)
    return str(product_id) in cart


def get_cart_item_count(session):
    cart = _sync_cart_with_products(session)
    return sum(cart.values())


def add_to_cart(session, product_id, quantity=1):
    cart = _sync_cart_with_products(session)
    product_key = str(product_id)
    if not Product.objects.filter(pk=product_id).exists():
        return
    current = int(cart.get(product_key, 0))
    new_qty = _normalize_for_add(current + _normalize_for_add(quantity))
    cart[product_key] = new_qty
    session[CART_SESSION_KEY] = cart
    session.modified = True


def update_cart_item(session, product_id, quantity):
    cart = _sync_cart_with_products(session)
    product_key = str(product_id)
    qty = _parse_update_quantity(quantity)
    if qty <= 0 or not Product.objects.filter(pk=product_id).exists():
        cart.pop(product_key, None)
    else:
        cart[product_key] = qty
    session[CART_SESSION_KEY] = cart
    session.modified = True


def remove_from_cart(session, product_id):
    cart = _sync_cart_with_products(session)
    cart.pop(str(product_id), None)
    session[CART_SESSION_KEY] = cart
    session.modified = True


def clear_cart(session):
    session[CART_SESSION_KEY] = {}
    session.modified = True


def get_cart_lines(session):
    cart = _sync_cart_with_products(session)
    if not cart:
        return [], Decimal('0.00')

    product_ids = []
    for key in cart:
        product_id = _parse_cart_key(key)
        if product_id is not None:
            product_ids.append(product_id)

    products = Product.objects.in_bulk(product_ids)

    lines = []
    total = Decimal('0.00')

    for product_key, quantity in cart.items():
        product_id = _parse_cart_key(product_key)
        if product_id is None:
            continue
        product = products.get(product_id)
        if not product:
            continue
        qty = int(quantity)
        line_total = product.price * qty
        lines.append({
            'product': product,
            'quantity': qty,
            'line_total': line_total,
        })
        total += line_total

    return lines, total

from shop.cart import get_cart_item_count


def cart(request):
    return {
        'cart_item_count': get_cart_item_count(request.session),
    }

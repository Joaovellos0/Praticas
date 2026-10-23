from .cart import Cart


def carrinho_context(request):
    cart = Cart(request)
    return {
        "cart": cart,
        "cart_total_items": len(cart),
        "cart_total_price": cart.get_total_price(),
    }

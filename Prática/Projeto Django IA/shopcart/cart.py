from decimal import Decimal
from products.models import Guitarra

CART_SESSION_ID = "carrinho"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, guitarra, quantidade=1, override_quantity=False):
        guitarra_id = str(guitarra.id)
        if guitarra_id not in self.cart:
            self.cart[guitarra_id] = {
                "quantidade": 0,
                "preco": str(guitarra.preco),
            }

        if override_quantity:
            self.cart[guitarra_id]["quantidade"] = int(quantidade)
        else:
            self.cart[guitarra_id]["quantidade"] += int(quantidade)

        if self.cart[guitarra_id]["quantidade"] <= 0:
            self.remove(guitarra_id)
        else:
            self.save()

    def remove(self, guitarra_id):
        guitarra_id = str(guitarra_id)
        if guitarra_id in self.cart:
            del self.cart[guitarra_id]
            self.save()

    def update(self, guitarra_id, quantidade):
        self.add(guitarra=Guitarra.objects.get(id=guitarra_id), quantidade=quantidade, override_quantity=True)

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    def __iter__(self):
        guitarra_ids = [int(gid) for gid in self.cart.keys()]
        guitarras = {g.id: g for g in Guitarra.objects.filter(id__in=guitarra_ids).select_related("marca")}
        
        # Faz cópia para não alterar a estrutura original durante a iteração
        cart_copy = dict(self.cart)
        for guitarra_id, item in cart_copy.items():
            gid = int(guitarra_id)
            if gid in guitarras:
                item_data = dict(item)
                item_data["guitarra"] = guitarras[gid]
                item_data["preco"] = Decimal(item["preco"])
                item_data["subtotal"] = item_data["preco"] * item_data["quantidade"]
                item_data["id"] = gid
                yield item_data
            else:
                # Se a guitarra foi deletada do banco, remove do carrinho
                self.remove(guitarra_id)

    def __len__(self):
        return sum(item["quantidade"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["preco"]) * item["quantidade"]
            for item in self.cart.values()
        )

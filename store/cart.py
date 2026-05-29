from .models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, variant=None, price=None):
        key = f"{product_id}_{variant or 'default'}"
        if key not in self.cart:
            self.cart[key] = {
                'product_id': product_id,
                'quantity': 0,
                'variant': variant,
                'price': price,
            }
        self.cart[key]['quantity'] += quantity
        if price:
            self.cart[key]['price'] = price
        self.save()

    def remove(self, key):
        if key in self.cart:
            del self.cart[key]
            self.save()

    def update(self, key, quantity):
        if key in self.cart:
            if quantity <= 0:
                self.remove(key)
            else:
                self.cart[key]['quantity'] = quantity
                self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[CART_SESSION_KEY]
        self.save()

    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}
        for key, item in self.cart.items():
            product = products.get(item['product_id'])
            if product:
                price = item.get('price') or product.get_final_price()
                yield {
                    'key': key,
                    'product': product,
                    'quantity': item['quantity'],
                    'variant': item.get('variant'),
                    'price': price,
                    'total': price * item['quantity'],
                }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}
        total = 0
        for item in self.cart.values():
            product = products.get(item['product_id'])
            if product:
                price = item.get('price') or product.get_final_price()
                total += price * item['quantity']
        return total

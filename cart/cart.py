

class Cart():
    def __init__(self, request):
        self.session = request.session

        #get current session key if it exists
        cart = self.session.get('session_key')

        #if user is new, no session key, need to create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

    #make cart is available on all pages
        self.cart = cart


def add(self, product):
    product_id = str(product.id)

    #logic if they have already added to cart
    if product_id in self.cart:
        pass
    else:
        self.cart[product_id] = {'price': str(product.price)}
    
    self.session.modified = True


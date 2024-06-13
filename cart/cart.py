from store.models import Product, Profile
import datetime

class Cart():
    def __init__(self, request):
        self.session = request.session
        #get request
        self.request = request

        #get current session key if it exists
        cart = self.session.get('session_key')

        #if user is new, no session key, need to create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

    #make cart is available on all pages
        self.cart = cart


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #logic if they have already added to cart
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        
        self.session.modified = True

        #deal with login users
        if self.request.user.is_authenticated:
            #get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            #convert single ' quotation to "double quotation,
            #cause we convert to JSON and JSOn doesnt work with single quotation
            carty = str(self.cart)
            carty = carty.replace("\'","\"")

            #save the modified cart to Profile Model
            current_user.update(old_cart = carty)


    def __len__(self):
        return len(self.cart)
    


    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()

        #use ids to lookup products from database
        products = Product.objects.filter(id__in=product_ids)

        #return products of result
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities
    

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart

        #update dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        #delete from dictionary of cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True


    def cart_total(self):
        #get product ids
        product_ids = self.cart.keys()
        #look up those keys in dictionary of product models
        products = Product.objects.filter(id__in=product_ids)
        #get quantities
        quantities = self.cart
        total = 0

        for key,value in quantities.items():
            #convert key string to int
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:

                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total

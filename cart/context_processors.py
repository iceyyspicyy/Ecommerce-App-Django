from .cart import Cart

#create a context processor to make cart available on all the pages of the web application
def cart(request):
    #return default data from our cart
    return{'cart': Cart(request)}
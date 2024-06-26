from django.shortcuts import render, get_object_or_404
from store.models import Product
from .cart import Cart
from django.http import JsonResponse
from django.contrib import messages 

def cart_summary(request):
    #get cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    # get cart
    cart = Cart(request)
    #test for post
    if request.POST.get('action') == 'post':
        #get stuffs
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        #look up product in database
        product = get_object_or_404(Product, id=product_id)

        #save to session
        cart.add(product=product, quantity=product_qty)
        
        #get cart quantity
        cart_quantity = cart.__len__()

        #return response
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Added to cart!")
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get stuffs
        product_id = int(request.POST.get('product_id'))
        #call delete function
        cart.delete(product=product_id)

        reponse = JsonResponse({'product':product_id})
        messages.success(request, "Item deleted successfully :)")

        return reponse



def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get stuffs
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        reponse = JsonResponse({'qty':product_qty})
        messages.success(request, "Cart updated successfully :)")

        return reponse
        #return redirect('cart_summary')
from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime
# Create your views here.
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get order
        order = Order.objects.get(id=pk)
        #get order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            if status == 'true':
                order = Order.objects.filter(id=pk)
                #update status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
              
            else:
                order = Order.objects.filter(id=pk)
                #update status
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('home')


        return render (request, 'payment/orders.html', {"order":order, "items":items})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')



def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            
            now = datetime.datetime.now()
            order.update(shipped=False)
              
           
            messages.success(request, "Shipping Status Updated")
            return redirect('home')
        return render(request, 'payment/shipped_dash.html', {"orders":orders})

    else:
        messages.success(request,"Access Denied!")
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
              
           
            messages.success(request, "Shipping Status Updated")
            return redirect('home')

        return render(request, 'payment/not_shipped_dash.html', {"orders":orders})
    else:
        messages.success(request,"Access Denied!")
        return redirect('home')


def payment_success(request):
    orders = Order.objects.filter(shipped=True)
    return render(request, 'payment/payment_success.html', {"orders":orders})

def process_order(request):
    if request.POST:
        #get cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        #get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        #get shipping stuffs session data
        my_shipping = request.session.get('my_shipping')

          #get order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        amount_paid = totals
        #create shippin address from session
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
     

        if request.user.is_authenticated:
            user = request.user
            #create order
            create_order = Order(user=user, full_name = full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            #add order items
            #get order ID
            order_id = create_order.pk
            #get product id
            for product in cart_products():
                #get prodcut id
                product_id = product.id
                #get sales price of prodct
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                #get quantiyy
                for key, value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value,price=price)
                        create_order_item.save()

            #delete our cart 
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete key
                    del request.session[key]



            messages.success(request,"Order Placed! Jingle Bells!")
            return redirect('home')
        else:
            create_order = Order(full_name = full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk
            #get product id
            for product in cart_products():
                #get prodcut id
                product_id = product.id
                #get sales price of prodct
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                #get quantiyy
                for key, value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value,price=price)
                        create_order_item.save()

            #delete our cart 
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete key
                    del request.session[key]

            #delete from database i.e. old_cart
            current_user = Profile.objects.filter(user__id = request.user.id)

            current_user.update(old_cart="")


            messages.success(request,"Order Placed! Jingle Bells!")
            return redirect('home')


    else:
        messages.success(request, "Access Denied!!")
        return redirect('home')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #checkout as login
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    
    else:
        #checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form":shipping_form})

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        #create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #check if user is logged in
        if request.user.is_authenticated:
            #get billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info":request.POST, "billing_form":billing_form})
        else:
            #not logged in
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info":request.POST, "billing_form":billing_form})



        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form":shipping_form})
    else:
        messages.success(request, "Access Denied!!")
        return redirect('home')
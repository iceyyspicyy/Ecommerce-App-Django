from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout

#for user registration the below 3 imports
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

#gives messages if its wrong when logging in
from django.contrib import messages
#can make multiple queries together
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    #detemine if text for search is filled
    if request.method == "POST":
        searched = request.POST['searched']
        #query the product in dbmodel
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #test for null
        if not searched:
            messages.success(request, "Item not found")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched':searched})
    
        
    else:
        return render(request, 'search.html', {})

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #shopping cart persistence stuff
            current_user = Profile.objects.get(user__id=request.user.id)

            #get their saved cart info
            saved_cart = current_user.old_cart

            #change database string to py dictionary
            if saved_cart:
                #convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #add the loaded dictionary to our session
                cart = Cart(request)

                #loop through the cart and add item from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, "You have successfully entered the verse!!")
            return redirect('home')
        else:
            messages.success(request, "Cant verify you! Are you a human or what? ")
            return redirect('login')

    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out! Adios....")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login the user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "User Created. Please fill your details")
            return redirect('update_info')
        else:
            messages.success(request, "Oops. Account registration failed")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, foo):
    #replace hyphen with space
    foo = foo.replace('-', ' ')
    #grab category from url
    try:
        #Look up category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, "Category invalid")
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    
    return render(request, 'category_summary.html', {'categories': categories})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)

            messages.success(request, "User has been updated!!")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, "You must be logged in first")
        return redirect('home')
    

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #check if they filled the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            #is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Password updated successfully.")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, "Must be logged in")
        return redirect('home')
    

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your Information has been updated!!")
            return redirect('home')
        return render(request, 'update_info.html', {'form':form})
    else:
        messages.success(request, "You must be logged in first")
        return redirect('home')

from django.contrib import admin
from .models import Category, Product, Customer, Order, Profile

#add the added things to the User 
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)

#mix profile info with user, code:
class ProfileInline(admin.StackedInline):
    model = Profile

#extend the user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username','first_name','last_name','email', 'date_joined']
    inlines = [ProfileInline]

#unregister the old wawy
admin.site.unregister(User)

#re-register the new way
admin.site.register(User, UserAdmin)

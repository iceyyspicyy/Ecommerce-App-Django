from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save  #automatically saved the profile for them after register

#create customer profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    #for cart persistance
    old_cart = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
#auto create a customer profile when user register from the app
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()

#automate the profile thing
post_save.connect(create_profile, sender=User)






    

# Categories of Product
class Category(models.Model):
    name = models.CharField(max_length=50)
    cat_image = models.ImageField(upload_to='uploads/category/', null=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


#customers
class Customer(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

#products model
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    #to determine sales stuff

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    def __str__(self):
        return self.name

#customer orders
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date = models.DateField(default= datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
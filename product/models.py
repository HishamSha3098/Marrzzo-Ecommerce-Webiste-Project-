from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created =models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name

class product_storage(models.Model) :
    storage = models.CharField(max_length=100)
    def __str__(self):
        return self.storage
         
class product_ram(models.Model) :
    ram = models.CharField(max_length=100)

    def __str__(self):
        return self.ram

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2)
    image1 = models.ImageField(upload_to='images/users/', default='images/users/pngwing.com_3.png')   
    image2 = models.ImageField(upload_to='images/users/', default='images/users/pngwing.com_3.png')
    image3 = models.ImageField(upload_to='images/users/', default='images/users/pngwing.com_3.png')
    brand = models.CharField(null=True,max_length=100)
    
    
    Category = models.ForeignKey(category, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    # Add other fields as necessary
    

class ProductVarient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ram = models.ForeignKey(product_ram,default="Nothing to Show",null=True,on_delete=models.CASCADE)
    storage = models.ForeignKey(product_storage,default="Nothing to Show",null=True,on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.product.name} ({self.ram} RAM, {self.storage} Storage) - Stock: {self.stock}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.name}"

class Ad_to_cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    coupen = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.FloatField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self):
        return self.code


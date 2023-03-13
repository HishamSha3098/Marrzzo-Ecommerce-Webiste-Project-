from django.db import models
from django.contrib.auth.models import User
from product.models import ProductVarient

# Create your models here.
class Payment(models.Model):
    user    =  models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id =   models.CharField(max_length=100)
    order_id = models.CharField(max_length=100,blank=True)
    payment_method = models.CharField(max_length=100)
    amount_paid     = models.CharField(max_length=100) #this is total amount paid
    created_at = models.DateTimeField(auto_now_add=True)
    status         = models.BooleanField(default=False)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name='orders')
    # address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    order_number = models.CharField(max_length=30)
    first_name = models.CharField(max_length=50, default='')
    last_name   = models.CharField(max_length=50, default='')
    phone_number= models.CharField(max_length=15, default='')
    email = models.EmailField(max_length=50, default='')
    address = models.CharField(max_length=50, default='',null=True)
    
    Payment_id = models.CharField(max_length=50, default='',null=True)
    
    state =   models.CharField(max_length=50, default='',null=True)
    city =   models.CharField(max_length=50, default='')
    country =   models.CharField(max_length=50, default='',null=True)
    post_code =   models.IntegerField(default=0,null=True)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    order_discount = models.FloatField(default=0,null=True)
    
    status = models.CharField(max_length=50,choices=STATUS,default='Order Confirmed')
    # coupen = models.FloatField(default=0,null=True)
    is_ordered = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    return_reason = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'



class OrderProduct(models.Model) :
    payment= models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True,related_name='order_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='order_product')

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVarient,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    product_price = models.FloatField()
    grand_total = models.FloatField(null=True)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





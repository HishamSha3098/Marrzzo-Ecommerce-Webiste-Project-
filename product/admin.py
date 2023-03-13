from django.contrib import admin
from .models import Product,Wishlist,category,Ad_to_cart,product_ram,product_storage,Coupon

# Register your models here.

admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(category)
admin.site.register(Ad_to_cart)
admin.site.register(product_ram)
admin.site.register(product_storage)
admin.site.register(Coupon)
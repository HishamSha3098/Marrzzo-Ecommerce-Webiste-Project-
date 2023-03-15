from django.shortcuts import render,redirect
from product.models import Ad_to_cart





def context_values(request) :

    try:
        cart_items = Ad_to_cart.objects.filter(user=request.user)
        total = sum(item.product.product.offer_price * item.quantity for item in cart_items)
        
        item_count = cart_items.count()
    except:
        cart_items=""
        total=0
        item_count=0

    context = {
        'cart_items':cart_items,
        'total': total,
        'item_count':item_count
    }

    return context
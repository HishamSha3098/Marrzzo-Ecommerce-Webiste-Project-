from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.order, name='checkout'),
    path('proceed-to-pay/', views.razorpaycheck, name='proceed-to-pay'),
    path('place-order/', views.place_order, name='placeorder'),
    path('invoice/<str:order_number>/', views.invoice, name='invoice'),

    path('my_orders/<str:order_number>/', views.my_orders, name='myorders'),
    path('cancel_orders/<str:order_number>/', views.cancel_order, name='cancelorders'),

    


    
    # Add other URL patterns as necessary
]

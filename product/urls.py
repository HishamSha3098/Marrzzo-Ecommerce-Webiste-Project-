from django.urls import path
from . import views

urlpatterns = [
    path('product_list/<int:id>/', views.product_list, name='product_list'),
    path('product_view/<int:id>', views.product_detail, name='product_view'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart/',views.update_cart,name="update_cart"),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_coupen/',views.add_coupon,name="add_coupen"),
    path('price_filter/',views.product_filter,name='price_filter'),
    path('checkout/',views.checkout,name='checkout'),
    path('viewall-coupen/',views.viewall_coupen,name='viewall_coupen')


    # Add other URL patterns as necessary
]

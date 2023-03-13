from django.urls import path
from . import views

urlpatterns = [
  path('admin_login/', views.adminLogin, name="admin_login"),
  path('add-category/', views.add_category, name="add_category"),
  path('view_category/',views.view_category,name='view_category'),
  path('edit_category/<int:pid>/',views.edit_category,name='edit_category'),
  path('delete_category/<int:pid>/',views.delete_category, name="delete_category"),
  path('add_product/',views.add_product, name="add_product"),
  path('view_product/',views.view_product, name='view_product'),
  path('delete_product/<int:pid>/', views.delete_product, name="delete_product"),
  path('admin_panel/', views.admin_panel, name="adminpanel"),
  path('user_manage/', views.user_manage, name="usermanage"),
  path('user_block/<int:u_id>', views.user_block, name="userblock"),
  path('edit_product/<int:pid>',views.edit_product, name="edit_product"),
  path('order_view/',views.order_view, name="order_vew"),
  path('orders/<int:order_id>/update_status/', views.update_order_status, name='update_order_status'),
  path('view_coupen/', views.view_coupen, name='viewcoupen'),
  path('create_coupen/', views.create_coupen, name='create_coupen'),
  path('update_coupen/<int:coupen_id>', views.update_coupen, name='update_coupen'),
  path('delete_coupen/<int:coupen_id>', views.delete_coupen, name='delete_coupen'),









 





]
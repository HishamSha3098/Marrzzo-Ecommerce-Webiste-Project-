from django.urls import path
from .import views
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
   
    path('',views.home,name="home"),
    # path('chat/<str:room_name>/', views.chat, name='chat'),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('resend_otp/<str:username>',views.resend_otp,name="resend"),
    path('item_view/',views.item_view,name="item_view"),
    path('user_profile/',views.user_profile,name="userprofile"),
    path('edit_profile/',views.edit_profile,name="editprofile"),
	path('search/',views.search_user,name="search"),
    path('change_password/',views.change_password,name="changepassword"),
	path('404_error/',views.errorpage,name="errorpage"),
	# path('Add_address/',views.Add_new_address,name="Add_address"),

    path("password-reset/", 
    	PasswordResetView.as_view(template_name='flip/password_reset.html'),
    	name="password_reset"),

	path("password-reset/done/", 
		PasswordResetDoneView.as_view(template_name='flip/password_reset_done.html'), 
		name="password_reset_done"),

	path("password-reset-confirm/<uidb64>/<token>/", 
		PasswordResetConfirmView.as_view(template_name='flip/password_reset_confirm.html'), 
		name="password_reset_confirm"),

	path("password-reset-complete/", 
		PasswordResetCompleteView.as_view(template_name='flip/password_reset_complete.html'), 
		name="password_reset_complete"),
   
    
]
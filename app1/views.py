from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from .forms import updateprofile,profileupdate,OrderForm
from .models import userprofile,Address
from order.models import Order

# from .forms import CreateUserForm

# from django.views.decorators.cache import never_cache


import random
from. models import UserOTP
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import category,Ad_to_cart,Product
from django.db.models import Q


# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from .models import Message
# import json




# Create your views here.


# @login_required(login_url='login')

def home(request) :
    
    if request.user.is_authenticated:
        cart_items = Ad_to_cart.objects.filter(user=request.user)
        total = sum(item.product.product.offer_price * item.quantity for item in cart_items)
        cart = Ad_to_cart.objects.filter(user=request.user)  
        item_count = cart.count()
        print('helow its me')
        print(item_count)
        allcategory = category.objects.all()
        return render(request,"flip/index.html",locals())
    else :
        allcategory = category.objects.all()
        return render(request,"flip/index.html",locals())
    
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def register(request):
    if request.user.is_authenticated:
        return redirect(home)
    usr = None
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        
        if get_otp:
            
            get_usr = request.POST.get('usr')
            
            usr=User.objects.get(username=get_usr)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                print('otp ok')
                usr.is_active=True
                usr.save()
                
                messages.success(request,f'Account is created for {usr.first_name}')
                return redirect('login')
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'flip/sign-in.html',{'otp':True,'usr':usr})
        first_name = request.POST['name']
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        confirmpass = request.POST['confirmpass'] 
        form = User.objects.create_user(username=username,password=password,email=email)
        if form is not None:
            form.save()
       #      email=form.cleaned_data.get('email')
       #      username=form.cleaned_data.get('username')
            usr=User.objects.get(username=username)
       #      print(usr)
       #      usr.email=email
            usr.first_name=first_name
            usr.is_active=False
            usr.save()
            usr_otp=random.randint(100000,999999)
            print(usr_otp)
            
            UserOTP.objects.create(user=usr,otp=usr_otp)
            mess=f'Hello\t{usr.first_name},\nYour OTP is {usr_otp}\nThanks!'
            send_mail(
                    "welcome to DOT.SHOP your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently=False
                )
            return render(request,'flip/register.html',{'otp': True, 'usr': usr}) 
                # print("OTP sent to:", usr.email)
       #      return render(request,'index.html'{'otp':True,'usr':usr})
        else:
            errors = form.errors
            print(form.errors)
    else:
            errors = ''
#     form=CreateUserForm()
    context = {'errors': errors}
    return render(request,'flip/register.html',context)




def resend_otp(request,username):
       get_usr = username
       
      
       if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
              usr = User.objects.get(username=get_usr)
              usr_otp = random.randint(100000, 999999)
              UserOTP.objects.create(user = usr, otp = usr_otp)
              mess = f"Hello, {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

              send_mail(
                     "Welcome to DOT.SHOP - Verify Your Email",
                     mess,
                     settings.EMAIL_HOST_USER,
                     [usr.email],
                     fail_silently = False
                     )
              messages.info(request,f'Resend successfull')
              return render(request,'flip/register.html',{'otp': True, 'usr': usr})

       return HttpResponse("error Can't Send OTP ")
        
@cache_control(no_cache=True,must_revalidate=True,no_store=True)        
def login(request) :
       if request.method == 'POST' :
              username = request.POST['email']
              password = request.POST['password']

              user = auth.authenticate(username=username,password=password)

              if user is not None :
                     auth.login(request,user)
                     if userprofile.objects.filter(user=request.user) :
                        return redirect(home) 
                     else:
                        userprofile.objects.create(user=request.user)

                        return redirect(home)
              else :
                     messages.error(request,'User name or Password is incorrect')  
                     return redirect(login)
       else :   
              return render(request,"flip/sign-in.html")
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='login')
def logout(request) :
       auth.logout(request)
       return redirect(home)

def item_view(request) :
    return render(request,'single.html')


def user_profile(request) :
    cart = Ad_to_cart.objects.filter(user=request.user)  
    item_count = cart.count()
    Userprofile = get_object_or_404(userprofile, user=request.user)
    orderitem = Order.objects.filter(user=request.user)
    order_count = orderitem.count()
    return render(request,'flip/userprofile.html',locals())

def edit_profile(request) :
    if userprofile.objects.filter(user=request.user) :
        Userprofile = get_object_or_404(userprofile, user=request.user)
    else :
        Userprofile = userprofile.objects.create(user=request.user)
    if request.method == 'POST' :
        user_form = updateprofile(request.POST, instance=request.user)
        profile_form = profileupdate(request.POST,request.FILES,instance=Userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            
            user_form.save()
            profile_form.save()
            messages.success(request,'profile updated successfuly')
            return redirect(edit_profile)
        else :
            messages.error(request,'there was an error while updating your profile')
    else :
        user_form = updateprofile(instance=request.user)
        profile_form = profileupdate(instance=Userprofile)
    cart = Ad_to_cart.objects.filter(user=request.user)  
    item_count = cart.count()    
    return render(request,'flip/editprofile.html',{'user_form':user_form, 'profile_form':profile_form ,'Userprofile':Userprofile,'item_count':item_count})
    

def change_password(request) :
    
    if request.method=='POST':
        current_password=request.POST["current_password"]
        new_password=request.POST["new_password"]
        confirm_password=request.POST["confirm_password"]
        user=User.objects.get(username__exact=request.user.username)
        if new_password==confirm_password:
            #check password in built function -stored in hashed format
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                auth.logout(request)
                messages.success(request,"Password updated successfully")
                return redirect(login)

            messages.error(request,"Please enter valid current password")
            return redirect('changepassword')
        else:
            messages.error(request,"Password does not match")
            return redirect('changepassword')
    
    return render(request,'flip/changepassword.html')


def search_user(request) :
    searching = request.GET['search']
    if searching :
        product = Product.objects.order_by('id').filter(Q(name__icontains=searching)|Q(offer_price__icontains=searching)|Q(brand__icontains=searching))
    return render(request,'flip/category.html',{'products' : product})


def errorpage(request) :
    return render(request,'flip/404.html')


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Save message to database
#         await self.save_message(message)

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': event['message']
#         }))

#     @sync_to_async
#     def save_message(self, message):
#         Message.objects.create(
#             room=self.room_name,
#             message=message
#         )



# def chat(request, room_name):
#     return render(request, 'flip/chat.html', {
#         'room_name': room_name
#     })



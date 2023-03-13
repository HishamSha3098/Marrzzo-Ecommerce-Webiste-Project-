from django.shortcuts import render,redirect,HttpResponse
from .models import Order,OrderProduct,Payment
import datetime
from product.models import Coupon,Ad_to_cart,Product,ProductVarient
from app1.models import Address
from app1.forms import OrderForm
from django.contrib import messages
from django.http import JsonResponse

from django.core.mail import send_mail
from django.conf import settings
import razorpay




# Create your views here.


def order(request) :
    data=None
    coupon=0
    current_user = request.user
    cart_items = Ad_to_cart.objects.filter(user=current_user)
    total = sum(item.product.product.offer_price * item.quantity for item in cart_items)
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        coupon = Coupon.objects.get(id=coupon_id)
        discount = int(total)-int(coupon.discount)
    else:
        discount = total
    if request.method == 'POST':
        if request.POST.get('form_type') == 'form1':
            instance = Address.objects.create(user=current_user)
            form = OrderForm(request.POST, instance=instance)
            print('this is form')
            if form.is_valid():
                print('form valid')
                form.save()
                messages.success(request,'Form is success')
                return redirect('checkout')
                # redirect to success page or do something else
            else:
                print(form.errors)
                print('hai')
        else :
            check = request.POST['ad']
            print(check)
            check = check.split('-')
            user = current_user
            data = Order()
            
            data.user = current_user
            data.first_name = check[0]
            
            data.phone_number = check[6]
            data.email = user.email
            data.address = check[1]
            
            data.state = check[4]
            
            data.city = check[2]
            data.country = check[5]
            data.post_code = check[3]
            data.order_total = discount

            data.save()        
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") 
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()  

            
    

    print('function started')
    print(current_user)
    
    
    form = OrderForm()
    
    AddRess = Address.objects.filter(user=current_user)
    order=None
    
    if data:
        print(data, '--------------------------------------------------------------')
        order = data.order_number
        print(data.order_number)
    
    context = {
    'order':order,
    'cart_items':cart_items,
    'total':total,
    'Address' : AddRess,
    'discount' : discount,
    'sub_total' : total,
    'coupon':coupon,
    # 'order_number':order_number,
    'form' :form
    }
    return render(request, 'flip/checkout.html', context)


def razorpaycheck(request) :
    print("im in raxor")
    current_user = request.user
    cart_items = Ad_to_cart.objects.filter(user=current_user)
    total = sum(item.product.product.offer_price * item.quantity for item in cart_items)
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        coupon = Coupon.objects.get(id=coupon_id)
        discount = int(total)-int(coupon.discount)
    else:
        discount = total
    print(discount)
    order_id = request.GET['orderid']
    print(order_id,'------------------------ss')
    order=Order.objects.get(order_number=order_id,is_ordered=False)
    order_values = {                                              
        'fname' : order.first_name,
        'email' : order.email,
        'address':order.address,
        'city' : order.city,
        'state':order.state,
        'country' : order.country,
        'pin_code' : order.post_code,
        'phone' :order.phone_number,
        'amount' :order.order_total,
        'order_id' :order.order_number
    }
    return JsonResponse({'values' :order_values})


def place_order(request):

    print('im in place order')
    
    current_user = request.user
    

    payment_mode = request.POST.get('payment_mode')
    order_id = request.POST.get('order_id')
    amount = request.POST.get('amount')
    payment_id = request.POST.get('payment_id')
    
    payment = Payment()
    payment.user=current_user
    payment.payment_id=payment_id
    payment.payment_method = payment_mode 
    payment.amount_paid = amount
    payment.save()


    Order.objects.filter(order_number=order_id).update(Payment_id=payment_id)
    order=Order.objects.get(order_number=order_id)


    cart_product = Ad_to_cart.objects.filter(user=current_user)

    for item in cart_product :

        OrderProduct.objects.create(

                order=order,
                user = current_user,
                payment = payment,
                product = item.product,
                quantity = item.quantity,
                product_price = item.product.product.offer_price,
                grand_total = payment.amount_paid

    
        )

        orderproduct = ProductVarient.objects.filter(id=item.product_id).first()
        orderproduct.stock = orderproduct.stock - item.quantity
        orderproduct.save()
    
    Ad_to_cart.objects.filter(user=current_user).delete()

    print("cart deleted")
    messages.success(request,"your order has placed")
    # mess=f'Hello\t{current_user.first_name},\nYour Order has been Placed,Thanks for shopping with us\nThanks!'
    # send_mail(
    #                  "Marrazzo - Order Placed",
    #                  mess,
    #                  settings.EMAIL_HOST_USER,
    #                  [current_user.email],
    #                  fail_silently = False
    #                  )
    if 'coupon_id' in request.session:
            del request.session['coupon_id']

    PayMode = request.POST.get('payment_mode')
    if (PayMode == "Paid by Razorpay"):
        return JsonResponse({"status" :"your order has placed"})
    
   
    
    return redirect('userprofile')


def my_orders(request,order_number) :
    ordernumber=Order.objects.get(user=request.user,order_number=order_number)
    print(ordernumber)
    orderitem = OrderProduct.objects.filter(user=request.user,order=ordernumber)
    order_count = orderitem.count()
    # print(orderitem.payment.payment_mode,"---------------------------------------")


    return render(request,'flip/order_product.html',locals())

def invoice(request,order_number) :
    ordernumber=Order.objects.get(user=request.user,order_number=order_number)
    print(ordernumber)
    orderitem = OrderProduct.objects.filter(user=request.user,order=ordernumber)
    order_count = orderitem.count()


    return render(request,'flip/invoice.html',locals())

def cancel_order(request,order_number) :

    client = razorpay.Client(auth=("rzp_test_wDSZWwmcRov4vw", "9oAya7f4mhQbmmJ2d67bCrkX"))
    order = Order.objects.get(order_number=order_number)
    payment_id = order.Payment_id
    amount = int(order.order_total)
    amount = amount*100
    print(amount,"this the amount")
    capture_data = {
    'amount': amount,  # amount to be captured in paise
    'currency': "INR"
        }
    
    captured_payment = client.payment.capture(payment_id,amount)

    

    if captured_payment['status'] == 'captured':

        print(client,'thisis client ,,,,,,,,,,,,,,,,,,,,,,,,,,')
        refund_data = {
        "payment_id": payment_id,
        "amount": amount,  # amount to be refunded in paise
        "currency": "INR",
        # enable speedy refund for instant refunds
                }

        # payment = client.payment.fetch(payment_id)
        # print(payment,'this is payment id and objext ---------------------------------')
        refund = client.payment.refund(payment_id, refund_data)
        if refund is not None:
            current_user=request.user
            Order.objects.filter(user=current_user,order_number=order_number).update(status='Cancelled')


            # mess=f'Hello\t{current_user.first_name},\nYour Product has been canceled,Money will be refunded with in 1 hour\nThanks!'
            # send_mail(
            #                 "Marrazzo - Cancel Product",
            #                 mess,
            #                 settings.EMAIL_HOST_USER,
            #                 [current_user.email],
            #                 fail_silently = False
            #                 )
        else :
            pass

    else :
        return HttpResponse("not captured")

    return redirect('userprofile')
    
from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,category,Ad_to_cart,Wishlist,Coupon
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import CouponForm
from django.core.paginator import Paginator
from django.http import JsonResponse



def product_list(request,id):

    if request.user.is_authenticated:
        cart_items = Ad_to_cart.objects.filter(user=request.user)
        total = sum(item.product.offer_price * item.quantity for item in cart_items)
        item_count = cart_items.count()

    else :
        cart_items=0    
        total= 0
        item_count=0
    if id ==0 :
        product = Product.objects.all()
        paginator = Paginator(product, 2) # divide the data into pages of 10 items each
        page_number = request.GET.get('page') # get the current page number from the URL query string
        products = paginator.get_page(page_number)
    else :
        Category = category.objects.get(id=id)
        product = Product.objects.filter(Category=Category)
        paginator = Paginator(product,1)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
    allcategory = category.objects.all()
    context ={
        'current_min_price': Product.objects.all().order_by('price').first().price,
        'current_max_price': Product.objects.all().order_by('-price').first().price,
        'products' :products,
        'allcategory' : allcategory,
        'cart_items' : cart_items,
        'total' :total,
        'item_count' :item_count
    }
    
    # Add filtering and sorting logic here
    return render(request, 'flip/category.html',context)
    
def product_detail(request,id):
    if request.user.is_authenticated:
        cart = Ad_to_cart.objects.filter(user=request.user)  
        item_count = cart.count()
        cart_items = Ad_to_cart.objects.filter(user=request.user)
        total = sum(item.product.offer_price * item.quantity for item in cart_items)
    product = Product.objects.get(id=id)
    
    # Add variation logic here
    return render(request, 'flip/detail.html', locals())
@login_required(login_url='login')
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)
        product = Product.objects.get(id=product_id)
        cart_item, created = Ad_to_cart.objects.get_or_create(
            user=request.user, product=product)
        cart_item.quantity = int(quantity)
        cart_item.save()
        # messages.success(request, f'{product.name} was added to your cart.')
        return redirect('cart')
    else:
        return redirect('home')
def update_cart(request) :
    if request.method == 'POST' :
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity',{})


        cart_item = Ad_to_cart.objects.get(user=request.user,product=product_id)
        cart_item.quantity = int(quantity)
        cart_item.save()
        return redirect('cart')

@login_required(login_url='login')
def cart(request):
    cart_items = Ad_to_cart.objects.filter(user=request.user)
    item_count = cart_items.count()
    # single_item = get_object_or_404(Ad_to_cart, id=request.product_id)
    total = sum(item.product.offer_price * item.quantity for item in cart_items)
    form = CouponForm
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        coupon = Coupon.objects.get(id=coupon_id)
        discount = int(total)-int(coupon.discount)
    else:
        discount = 0
    
    return render(request, 'flip/shopping-cart.html',locals())    

def remove_from_cart(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)
    Ad_to_cart.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'{product.name} was removed from your Cart.')
    return redirect('cart')

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'{product.name} was added to your wishlist.')
    else:
        messages.warning(request, f'{product.name} is already in your wishlist.')
    return redirect('product_view', id=product.id)

@login_required(login_url='login')
def wishlist(request):
    cart_items = Ad_to_cart.objects.filter(user=request.user)
    item_count = cart_items.count()
    total = sum(item.product.offer_price * item.quantity for item in cart_items)
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    return render(request,'flip/wishlist.html', locals())    
# Add other views as necessary
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'{product.name} was removed from your wishlist.')
    return redirect('wishlist')


def add_coupon(request):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code, valid_from__lte=now, valid_to__gte=now)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart',)

def product_filter(request):
    print(request.GET)
    min_price = (request.GET['minprice'])
    
    max_price = (request.GET['maxprice'])
    
    
    
    products=Product.objects.all()
    if min_price:
        products = products.filter(offer_price__gte=min_price)
    if max_price:
        products = products.filter(offer_price__lte=max_price)
   
    context = {
        'products': products,
        'min_price': Product.objects.all().order_by('price').first().offer_price,
        'max_price': Product.objects.all().order_by('-price').first().offer_price,
        'current_min_price': Product.objects.all().order_by('price').first().offer_price,
        'current_max_price': Product.objects.all().order_by('-price').first().offer_price
    }
    return render(request, 'flip/category.html', context)

def checkout(request) :
    return render(request,'flip/checkout.html')



def viewall_coupen(request) :
    allcoupen=Coupon.objects.all()

    return render(request,'flip/viewall-coupen.html',locals())
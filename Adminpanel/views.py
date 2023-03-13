from django.shortcuts import render,redirect,get_object_or_404
from product.models import category,Product,product_ram,product_storage,Coupon
from django.contrib import messages
from django.contrib.auth.models import User,auth
from order.models import Order
from app1.models import userprofile
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime, timedelta
from .forms import AddCoupen
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

def admin_panel(request) :
        if request.user.is_staff :
            total=0
            grand_total=0
            ordertotal=Order.objects.all()
            ordercount=ordertotal.count()
            deliver=Order.objects.filter(status='Delivered')
            deliver_count = deliver.count()
            users=User.objects.all()
            usercount=users.count()
            userprofiles=userprofile.objects.get(user=request.user)
            for item in ordertotal :
                total= total+item.order_total
                grand_total=total

            today = datetime.now()
            last_12_months = today - timedelta(days=365)
            data = Order.objects.filter(created_at__gte=last_12_months) \
                            .annotate(month=TruncMonth('created_at')) \
                            .values('month') \
                            .annotate(count=Count('id')) \
                            .order_by('month')

            months = [d['month'].strftime('%b %Y') for d in data]
            counts = [d['count'] for d in data]

        

            chart_data = {
                'months': months,
                'counts': counts,
                'ordercount' :ordercount,
                'grand_total' :grand_total,
                'usercount': usercount,
                'userprofiles':userprofiles,
                'deliver_count' : deliver_count
            }
            return render(request,'adminhtml/index.html',chart_data)
        else:
            return redirect('home')
    


def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        try:
            category.objects.create(name=name)
            msg = "Category added"
            # return redirect(view_category)

        except:
            msg2 = "dsdss"
    return render(request, 'adminhtml/Add-category.html', locals())

def view_category(request):
    Category= category.objects.all()
    paginator = Paginator(Category, 2) # divide the data into pages of 10 items each
    page_number = request.GET.get('page') # get the current page number from the URL query string
   
    if request.method == 'POST' :
        search = request.POST['search']
        
        allcategory =  category.objects.order_by('id').filter(Q(name__icontains=search))

    else :
         allcategory = paginator.get_page(page_number)
    return render(request,'adminhtml/view-category.html',locals())


def edit_category(request,pid):
    Category=category.objects.get(id=pid)
    if request.method=='POST':
        name=request.POST['name']
        Category.name=name
        Category.save()
        msg="category Updated"
        return redirect(view_category)
    return render(request,'adminhtml/update-category.html',locals())
    


def delete_category(request,pid):
    try :
        Category=category.objects.get(id=pid)
        Category.delete()

    except:
        pass
    



def add_product(request):
    categori = category.objects.all()
    ram = product_ram.objects.all()
    storage=product_storage.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        try:
            rams=request.POST['ram']
            storages=request.POST['storage']
            ramobj = product_ram.objects.get(id=rams)
            storagesobj = product_storage.objects.get(id=storages)
        except:
            rams=""
            storages=""
            ramobj=None
            storagesobj=None    
        brand=request.POST['brand']
        quantity = request.POST['quantity']
        discount = request.POST['discount']
        desc = request.POST['desc']
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        image3= request.FILES['image3']
        catobj = category.objects.get(id=cat)
        
        Product.objects.create(name=name, price=price, offer_price=discount,quantity=quantity,storage=storagesobj,ram=ramobj,brand=brand, Category=catobj, description=desc, image1=image1,image2=image2,image3=image3)
        messages.success(request, "Product added")
        return redirect(view_product)
    return render(request, 'adminhtml/product-add.html', locals())


def view_product(request):
    product = Product.objects.all()
    paginator = Paginator(product, 4) # divide the data into pages of 10 items each
    page_number = request.GET.get('page') # get the current page number from the URL query string
   
    if request.method == 'POST' :
        search = request.POST['search']
        
        allproduct =  Product.objects.order_by('id').filter(Q(name__icontains=search)|Q(offer_price__icontains=search)|Q(quantity__icontains=search))

    else :
         allproduct = paginator.get_page(page_number)
    return render(request, 'adminhtml/product-view.html', locals())


def edit_product(request, pid):
    product = Product.objects.get(id=pid)
    Category = category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        
        brand=request.POST['brand']
        quantity = request.POST['quantity']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image1 = request.FILES['image1']
            image2 = request.FILES['image2']
            image3 = request.FILES['image3']
            product.image1 = image1
            product.image2 = image2
            product.image3 = image3

            product.save()
        except:
            pass
        catobj = category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price, offer_price=discount,quantity=quantity,Category=catobj, description=desc,)
        messages.success(request, "Product Updated")
        return redirect(view_product)
    return render(request, 'adminhtml/edit-product.html', locals())


def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')


def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        try:
            if user.is_staff:
                auth.login(request, user)
                msg = "User login successfully"
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    return render(request, 'admin_login.html', dic)

def user_manage(request):
    users = User.objects.all()
    paginator = Paginator(users, 2) # divide the data into pages of 10 items each
    page_number = request.GET.get('page') # get the current page number from the URL query string
   
    if request.method == 'POST' :
        search = request.POST['search']
        
        allusers =  User.objects.order_by('id').filter(Q(first_name__icontains=search)|Q(email__icontains=search))

    else :
         allusers = paginator.get_page(page_number)
    return render(request,'adminhtml/user-manage.html',locals())


def user_block(request,u_id) :
    users=User.objects.get(id=u_id)
    if users.is_active == True :
        users.is_active= False
        users.save()
        return redirect(user_manage)
    else:
        
        users.is_active= True
        users.save()
        return redirect(user_manage)

def order_view(request) :
    order= Order.objects.all()
    paginator = Paginator(order, 4) # divide the data into pages of 10 items each
    page_number = request.GET.get('page') # get the current page number from the URL query string
   
    if request.method == 'POST' :
        search = request.POST['search']
        
        allorder =  Order.objects.order_by('id').filter(Q(first_name__icontains=search)|Q(order_number__icontains=search)|Q(status__icontains=search))

    else :
         allorder = paginator.get_page(page_number)
    return render(request,'adminhtml/order-view.html',{"allorder" :allorder})

def update_order_status(request, order_id):
    # get the order instance
    order = Order.objects.get(order_number=order_id)

    if request.method == 'POST':
        # get the chosen status option from the form
        new_status = request.POST['status']

        # update the status of the order
        order.status = new_status
        order.save()

        return redirect(order_view)

    # get the status options
    status_options = order.STATUS
    

    # pass the options to the context dictionary
    context = {
        'status_options': status_options
    }

    return render(request, 'adminhtml/order-status.html', context)



def view_coupen(request) :
    allcoupen=Coupon.objects.all()
    paginator = Paginator(allcoupen, 1) # divide the data into pages of 10 items each
    page_number = request.GET.get('page') # get the current page number from the URL query string
   
    if request.method == 'POST' :
        search = request.POST['search']
        allcoupen =  Coupon.objects.order_by('id').filter(Q(code__icontains=search)|Q(discount__icontains=search))

    else :
        allcoupen = paginator.get_page(page_number)

    return render(request,'adminhtml/coupen-view.html',locals())


def create_coupen(request) :
    if request.method == 'POST' :
        form=AddCoupen(request.POST)

        if form.is_valid :
            form.save()

            return redirect(view_coupen)

    else:
        form =AddCoupen()

    return render (request,'adminhtml/create-coupen.html',locals())


def update_coupen(request,coupen_id) :
    coupen =get_object_or_404(Coupon,id=coupen_id)
    if request.method == 'POST' :
        form=AddCoupen(request.POST,instance=coupen)

        if form.is_valid :
            form.save()

            return redirect(view_coupen)

    else:
        form =AddCoupen(instance=coupen)

    return render (request,'adminhtml/update-coupen.html',locals())


def delete_coupen(request,coupen_id) :
    Coupon.objects.get(id=coupen_id).delete()

    return redirect(view_coupen)




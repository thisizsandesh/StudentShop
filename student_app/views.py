from django.shortcuts import render, redirect, HttpResponse
from .models import Product, Cart, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
import random
import razorpay
from django.shortcuts import get_object_or_404, redirect

def home(request):
    context={}
    p=Product.objects.filter(is_active=True)
    context['products']=p
    return render(request,'index.html',context)

def product_details(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'product_details.html',context)

def register(request):
    context={}
    if request.method=="POST":
        uname=request.POST['suemail']
        upass=request.POST['supass1']
        upassed=request.POST['supass2']
        if uname=="" or upass=="" or upassed=="":
             context['errormsg']="Field cannot be empty"
             return render(request,'register.html',context)
        
        elif upass != upassed:
            context['errormsg']="Password didi not match"
            return render(request,'register.html',context)
        
        else:
            try:
                u=User.objects.create(username=uname,password=upass,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="user created successfully please log in"
                return render(request,'register.html',context)
            except Exception:
                context['errormsg']="Username already exist"
                return render(request,'register.html',context)
    else:
        if request.method=='GET':
          return render(request,'register.html')
        
def user_login(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upassword']
        if uname=="" or upass=="" :
             context['errormsg']="Field cannot be empty"
             return render(request,'index.html',context)
        
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errormsg']="Invalid username and password"
                return render(request,'index.html',context)
    else:
            return render(request,'login.html')
    
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('/home')

def cart(request):
    return render (request,'cart.html')


def addtocart(request, pid):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_instance = get_object_or_404(User, id=user_id)
        product_instance = get_object_or_404(Product, id=pid)

        cart_instance, created = Cart.objects.get_or_create(uid=user_instance, pid=product_instance)

        if created:
            messages.success(request, f"{product_instance.name} has been added to your cart.")
        else:
            messages.warning(request, f"{product_instance.name} is already in your cart.")

        return redirect('/home') 
    else:
        messages.error(request, "Error: You must be logged in to add items to the cart.")
        return redirect('/login') 


def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    s=0
    np=len(c)
    context={}
    for x in c:
        s=s+x.pid.price *x.qty
    context['n']=np
    context['products']=c
    context['total']=s
    return render(request,'cart.html',context)

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect ('/viewcart')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect("/viewcart")

def range(request):
    min=request.GET['umin']
    max=request.GET['umax']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print('order id ',oid)
    

    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(c)
    
    for x in c:

        s=s+x.pid.price*x.qty
        context={}
        context['n']=np
        context['products']=c
        context['total']=s
    return render(request,'placeorder.html',context)


def sort(request,abc):
    if abc == '0':
        col = 'price'
    
    else:
        col='-price'

    p=Product.objects.filter(is_active=True).order_by(col)

    context={}
    context['products']=p

    return render(request,"index.html",context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_O8sAGWhjhZI54X", "Fsty5BtDRoPu7GRhsvQ6e70p"))

    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render (request,'pay.html',context)





    
        


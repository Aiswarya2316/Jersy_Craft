from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User,auth
import datetime
from django.conf import settings
# import razorpay
from django.db.models import Avg
import math
import json
from django.views.decorators.csrf import csrf_exempt
import re
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
# from django.conf import settings
from django.http import JsonResponse
# from django.conf import settings
import razorpay
# import json
# from django.views.decorators.csrf import csrf_exempt







# Create your views here.

def get_usr(req):
    data=Register.objects.get(Email=req.session['user'])
    return data


def get_shop(req):
    data=Shopreg.objects.get(Email=req.session['shop'])
    return data

def get_product(req):
    data=Product.objects.get(shop=req.session['product'])
    return data



def login(req):
    if 'user' in req.session:
        return redirect(userhome)
    if 'admin' in req.session:
        return redirect(adminhome)
    if 'shop' in req.session:
        return redirect(viewpro)
    if 'deliveryss' in req.session:
        return redirect(deliverys)
    

    if req.method=='POST':
        Email=req.POST['Email']
        password=req.POST['password']
        try:
            data=Register.objects.get(Email=Email,password=password)
            req.session['user']=data.Email
            return redirect(userhome)
        except Register.DoesNotExist:
            admin=auth.authenticate(username=Email,password=password)
            if admin is not None:
                auth.login(req,admin)
                req.session['admin']=Email

                return redirect(viewshop)
            
            else:
                try:
                    data=Shopreg.objects.get(Email=Email,password=password)
                    req.session['shop']=data.Email

                    return redirect(viewpro)
                except Shopreg.DoesNotExist:

                    messages.warning(req, "INVALID INPUT !  ")
                    


        # messages.warning(req, "INVALID INPUT !")
    return render(req,'login.html')



def logout(req):
    if 'user' in req.session:
        # req.session.flush()
        del req.session['user']
    if 'admin' in req.session:
        del req.session['admin']
    if 'shop' in req.session:
        del req.session['shop']
    if 'deliveryss' in req.session:
        del req.session['deliveryss']
    return redirect(login)


def register(req):

    if req.method=='POST':
            name1=req.POST['name']
            email2=req.POST['Email']
            phonenumber3=req.POST['phonenumber']
            location4=req.POST['location']
            password5=req.POST['password']
        # try:
            data=Register.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,location=location4,password=password5)
            data.save()
             # Validate email
            subject = 'Registration details '
            message = 'Dear user your accound successfully registered ! ur account uname {}  and password {}'.format(name1,password5)
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email2]
            send_mail(subject, message, from_email, recipient_list,fail_silently=False)
            return redirect(login)
        # except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'user/register.html')


def shopregister(req):

    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['Email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['location']
        password5=req.POST['password']
        # try:
        data=Shopreg.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,location=location4,password=password5)
        data.save()
        return redirect(login)
        # except:
        #     messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'shop/shopregister.html')
    print(shopregister)

def delregister(req):

    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['Email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['rout']
        password5=req.POST['password']
    
        try:
            data=delivery.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,rout=location4,password=password5)
            data.save()
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'delivery/deliveryreg.html')
    print(delregister)




def userhome(req):
    if 'user' in req.session:
        data = Product.objects.all().order_by('-shop')[:4]
        data1 = Buy.objects.filter(user=get_usr(req)).order_by('-date_of_buying')[:2]  # Only get the latest 2 orders
        data2 = cart.objects.filter(user=get_usr(req)).order_by('-id')[:2]  # Get the latest 4 cart items

        return render(req, 'user/userhome.html', {'data': data, 'data1': data1, 'data2': data2})
    else:
        return redirect(login)



def adminhome(req):
    
    return render(req,'admin/adminhome.html')





def deliverys(req):
    
    return render(req,'delivery/deliveryhome.html')



def addpro(req):
    if req.method=='POST':
        name = req.POST['name']
        discription = req.POST['discription']
        price = req.POST['price']
        quantity = req.POST['quantity']
        offerprice = req.POST['offerprice']
        image = req.FILES['image']
        category=req.POST['category']
        category=Category.objects.get(pk=category)
        data=Product.objects.create(name=name,discription=discription,price=price,quantity=quantity,offerprice=offerprice,image=image,category=category, shop=get_shop(req))
        data.save()
    
        return redirect(viewpro)
    category=Category.objects.all()
    
    return render(req,'shop/addpro.html', {'category':category})

 
    
def viewpro(req):
    if 'shop' in req.session:
        data=Product.objects.filter(shop=get_shop(req))
    # data=Product.objects.all()
        return render(req,'shop/viewpro.html',{'data':data}) 
    

def edit(req,id):
    data=Product.objects.get(pk=id)
    if req.method=='POST':
        name1=req.POST['name']
        price=req.POST['price']
        offerprice=req.POST['offerprice']
        quantity=req.POST['quantity']
        Product.objects.filter(pk=id).update(name=name1,price=price,offerprice=offerprice,quantity=quantity)
        return redirect(viewpro)
    return render(req,'shop/edit.html',{'data':data})

def delete(req,id):
    data=Product.objects.get(pk=id)
    data.delete()
    return redirect(viewpro)

###profile of user
def profile(req):
    if 'user' in req.session:
        # data=Register.objects.get(Email=req.session['user'])
        return render(req,'user/userprofile.html',{'data':get_usr(req)})
    else:
        return redirect(login)
    

    

###profile update
def upload(req):
    if 'user' in req.session:
        try:
            data = Register.objects.get(Email=req.session['user'])
        except Register.DoesNotExist:
            return redirect(login)

        if req.method == 'POST':
            name = req.POST['name']
            phonenumber = req.POST['phonenumber']
            location = req.POST['location']
            if not re.match(r'^[789]\d{9}$', phonenumber):
                return render(req, 'user/updateprofile.html', {
                    'data': data,
                    'error_message': 'Invalid Contact Number'
                })
            Register.objects.filter(Email=req.session['user']).update(name=name, phonenumber=phonenumber, location=location)
            return redirect(profile)
        return render(req, 'user/updateprofile.html', {'data': data})

    else:

        return redirect(login)

def userviewproduct(req):
    data=Product.objects.all()
    return render(req,'user/userviewproduct.html',{'data':data})



def prodetails(req, id):
    try:
        data = Product.objects.get(pk=id)
        if req.method=='POST':
            user=get_usr(req)
            shop=data.shop
            message = req.POST['message']
            rating = req.POST['rating']
            submitted_at = req.POST['submitted_at']
        
            feedback=Feedback.objects.create(user=user,shop=shop,product=data,message=message,rating=rating,submitted_at=submitted_at)
            feedback.save()
        return render(req, 'user/prodetails.html', {'data': data})
    except Product.DoesNotExist:
        messages.error(req, "Product not found.")
        return redirect(userviewproduct)

def products_by_category(request, category_id):
    category = Category.objects.get(pk=id)
    products = Product.objects.filter(category=category)
    return render(request, 'user/userviewproduct.html', {'category': category, 'products': products})

def shopprodetails(req,id):
    data=Product.objects.get(pk=id)
    feedback = Feedback.objects.filter(product=data).order_by('-submitted_at')
    average_rating = feedback.aggregate(Avg('rating'))['rating__avg']
    rounded_average_rating = round(average_rating) if average_rating else None
    return render(req,'shop/shopprodetails.html',{'data':data,'feedback':feedback,'average_rating': rounded_average_rating})


def user_cart(req,id):
    if 'user' in req.session:
        product=Product.objects.get(pk=id)
        user=get_usr(req)
        qty=1
        try:
            dtls=cart.objects.get(product=product,user=user)
            dtls.quantity+=1
            dtls.save()
        except:
            data=cart.objects.create(product=product,user=user,quantity=qty)
            data.save()
        return redirect(user_view_cart)
    else:
        return redirect(login)
    
def user_view_cart(req):
    if 'user' in req.session:
        data=cart.objects.filter(user=get_usr(req))
        return render(req,'user/addtocart.html',{'data':data})
def qty_incri(req,id):
    data=cart.objects.get(pk=id)
    data.quantity+=1
    data.save()
    return redirect(user_view_cart)

def qty_decri(req,id):
    data=cart.objects.get(pk=id)
    if data.quantity>1:
        data.quantity-=1
        data.save()
    return redirect(user_view_cart)

def buynow1(req,id):
    if 'user' in req.session:
        product=Product.objects.get(pk=id)
        user=get_usr(req)
        quantity=1
        date=datetime.datetime.now().strftime("%x")
        price=product.price
        order=Buy.objects.create(product=product,user=user,quantity=quantity,date_of_buying=date,price=price)
        order.save()
    return redirect(orderdetails)

def buynow(req,id):
     if 'user' in req.session:
        cart_product=cart.objects.get(pk=id)
        product=cart_product.product
        user=get_usr(req)
        quantity=cart_product.quantity
        date=datetime.datetime.now().strftime("%x")
        price=cart_product.product.price
        order=Buy.objects.create(product=cart_product.product,user=user,quantity=quantity,date_of_buying=date,price=price)
        order.save()

        return redirect(user_view_cart)
     
def deleteitem(req,id):
    data=cart.objects.get(pk=id)
    data.delete()
    return redirect(user_view_cart)


def orderdetails(req):
    # Fetch the orders for the user and order them by date_of_buying in descending order
    data = Buy.objects.filter(user=get_usr(req))[::-1]
    return render(req, 'user/orderdetails.html', {'data': data})




def viewshop(req):
    data=Shopreg.objects.all()
    return render(req,'admin/viewshop.html',{'data':data})


def aboutus(req):
    
    return render(req,'user/aboutus.html')

def contact(req):
    
    return render(req,'user/contact.html')

def service(req):
    
    return render(req,'user/service.html')

def bookinghistry(req):
    #  if 'shop' in req.session:
    l=[]
    data=Product.objects.filter(shop=get_shop(req))
    for i in data:
        data1=Buy.objects.filter(product=i)
        l.append(data1)
    print(l)
    # data1=delivery.objects.all()
    return render(req,'shop/bookinghistry.html',{'data':l})




def product_search(request):
    query = request.GET.get('query') 
    products = []
    if query:
        products = Product.objects.filter(name__icontains=query)
        
    return render(request, 'user/product_search.html', {'products': products, 'query': query})

def pro_search(request):
    query = request.GET.get('query') 
    products = []
    if query:
        products = Product.objects.filter(name__icontains=query)
        
    return render(request, 'shop/pro_search.html', {'products': products, 'query': query})




#####payment#######

def home(request):
    return render(request, "user/payment.html")


def order_payment(request, id):
    # Fetch the product based on product_id
        product = Product.objects.get (pk=id)

        name = product.name
        amount = product.price  # Get price directly from the product

        # Razorpay client setup
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create Razorpay order
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id = razorpay_order["id"]

        # Save the order in the database
        order = Order.objects.create(
            name=name, 
            amount=amount, 
            provider_order_id=order_id,
            product=product
        )
        order.save()

        return render(
            request,
            "user/payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
                "product": product,  # Pass product data to the template
            },
        )
    #  return render(request, "user/payment.html", {"product": product})



# def order_payment(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         amount = request.POST.get("amount")
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         razorpay_order = client.order.create(
#             {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
#         )
#         order_id=razorpay_order['id']
#         order = Order.objects.create(
#             name=name, amount=amount, provider_order_id=order_id
#         )
#         order.save()
#         return render(
#             request,
#             "user/payment.html",
#             {
#                 "callback_url": "http://" + "127.0.0.1:8000" + "razorpay/callback",
#                 "razorpay_key": settings.RAZORPAY_KEY_ID,
#                 "order": order,
#             },
#         )
#     return render(request, "user/payment.html")


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status})   # callback giving html page
            #  or  return redirect(function name of callback giving html page)
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status})  # callback giving html page
            #  or  return redirect(function name of callback giving html page)

    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})  # callback giving html page
        #  or  return redirect(function name of callback giving html page)
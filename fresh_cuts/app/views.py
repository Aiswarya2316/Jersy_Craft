from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User,auth
import datetime
from django.conf import settings
from django.db.models import Avg
import math
import json
from django.views.decorators.csrf import csrf_exempt
import re
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import JsonResponse
import razorpay


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
    return render(req,'login.html')



def logout(req):
    if 'user' in req.session:
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
            data=Register.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,location=location4,password=password5)
            data.save()
            return redirect(login)
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'user/register.html')


def shopregister(req):
    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['Email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['location']
        password5=req.POST['password']
        data=Shopreg.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,location=location4,password=password5)
        data.save()
        return redirect(login)
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


def profile(req):
    if 'user' in req.session:
        return render(req,'user/userprofile.html',{'data':get_usr(req)})
    else:
        return redirect(login)
    

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

# def prodetails(req, id):
#     try:
#         data = Product.objects.get(pk=id)
#         colors = ["Red", "Blue", "Green", "Black", "White", "Yellow"]
#         sleeve_options = ["Sleeve", "Non-Sleeve"]

#         if req.method == 'POST':
#             user = get_usr(req)
#             shop = data.shop
#             message = req.POST['message']
#             rating = req.POST['rating']
#             submitted_at = req.POST['submitted_at']
             

#             feedback = Feedback.objects.create(
#                 user=user, shop=shop, product=data, 
#                 message=message, rating=rating, submitted_at=submitted_at  # Save to DB
#             )
#             feedback.save()

#         return render(req, 'user/prodetails.html', {
#             'data': data, 
#             'colors': colors, 
#             'sleeve_options': sleeve_options
#         })
#     except Product.DoesNotExist:
#         messages.error(req, "Product not found.")
#         return redirect(userviewproduct)
def prodetails(req, id):
    try:
        data = Product.objects.get(pk=id)
        product_images = [
            {"color": img.color, "sleeve_type": img.sleeve_type, "image": img.image.url}
            for img in data.images.all()
        ]
        print(product_images)
        colors = list(set([img["color"] for img in product_images]))
        sleeve_options = list(set([img["sleeve_type"] for img in product_images]))

        if req.method == 'POST':
                    user = get_usr(req)
                    shop = data.shop
                    message = req.POST['message']
                    rating = req.POST['rating']
                    submitted_at = req.POST['submitted_at']
                    

                    feedback = Feedback.objects.create(
                        user=user, shop=shop, product=data, 
                        message=message, rating=rating, submitted_at=submitted_at  # Save to DB
                    )
                    feedback.save()

        return render(req, 'user/prodetails.html', {
            'data': data,
            'colors': colors,
            'sleeve_options': sleeve_options,
            'product_images': product_images  # Pass as a proper JSON object
        })
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


def user_cart(req, id):
    if 'user' in req.session:
        product = Product.objects.get(pk=id)
        user = get_usr(req)
        qty = 1
        try:
            dtls = cart.objects.get(product=product, user=user)
            dtls.quantity += 1  # Increment quantity
            dtls.save()
        except cart.DoesNotExist:
            cart.objects.create(product=product, user=user, quantity=qty)

        return redirect(user_view_cart)
    else:
        return redirect(login)

    

def user_view_cart(req):
    if 'user' in req.session:
        data = cart.objects.filter(user=get_usr(req))
        return render(req, 'user/addtocart.html', {'data': data})
    else:
        return redirect(login)  # Ensure it redirects if user is not logged in

    

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


import datetime

def buynow1(req, id):
    if 'user' in req.session:
        product = Product.objects.get(pk=id)
        user = get_usr(req)
        quantity = 1
        date = datetime.datetime.now().strftime("%x")
        price = product.price

        # Get selected color and sleeve type from request
        selected_color = req.GET.get("color", "")  
        selected_sleeve = req.GET.get("sleeve", "")  

        # Create the order with selected options
        order = Buy.objects.create(
            product=product,
            user=user,
            quantity=quantity,
            date_of_buying=date,
            price=price,
            color=selected_color,
            sleeve_type=selected_sleeve
        )
        order.save()

    return redirect(orderdetails)



import datetime

def buynow(req):
    if 'user' in req.session:
        user = get_usr(req)
        cart_items = cart.objects.filter(user=user)

        if not cart_items.exists():
            return redirect(user_view_cart)  # Redirect if cart is empty

        date = datetime.datetime.now().strftime("%x")
        total_price = sum(item.total_price() for item in cart_items)  # Calculate total price
        amount_in_paise = int(total_price * 100)  # ✅ Convert to paise (integer)

        # Create an order entry
        order = Order.objects.create(
            name=user.name,
            amount=total_price,  # Store amount in INR
            provider_order_id="TEMP_ORDER_ID",  # Update after Razorpay order creation
            payment_id="",
            signature_id="",
            status="Pending"
        )

        return render(req, 'user/payment.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'amount_in_paise': amount_in_paise,  # ✅ Pass amount in paise
            'order': order
        })
    else:
        return redirect(login)




def deleteitem(req,id):
    data=cart.objects.get(pk=id)
    data.delete()
    return redirect(user_view_cart)


def orderdetails(req):
    if 'user' in req.session:
        user = get_usr(req)
        orders = Buy.objects.filter(user=user).order_by('-id')  # Fetch user's orders
        return render(req, "user/orderdetails.html", {"orders": orders})
    else:
        return redirect(login)



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
    l=[]
    data=Product.objects.filter(shop=get_shop(req))
    for i in data:
        data1=Buy.objects.filter(product=i)
        l.append(data1)
    print(l)
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

def bookinghistory(req):
    if 'user' in req.session:
        user = get_usr(req)  # Get the logged-in user
        
        # Fetch direct purchases from Buy model
        buy_orders = Buy.objects.filter(user=user)

        # Fetch successful Razorpay orders
        successful_orders = Order.objects.filter(user=user, status="SUCCESS")
        user = Register.objects.first()  # Get any user
        orders = Order.objects.filter(user=user, status="SUCCESS")

        print(orders) 

        print("User:", user)  # Debugging
        print("Successful Orders:", successful_orders)  # Debugging output

        return render(req, 'user/bookinghistory.html', {
            'buy_orders': buy_orders, 
            'successful_orders': successful_orders
        })
    else:
        return redirect(login)






def home(request):
    return render(request, "user/payment.html")

def order_payment(request, id):
    if "user" not in request.session:
        return redirect(login)  # Ensure user is logged in

    user = get_usr(request)  # 🔥 Get the logged-in user correctly

    product = Product.objects.get(pk=id)
    name = product.name
    amount = product.price  

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create(
        {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
    )
    
    order_id = razorpay_order["id"]
    
    # 🔥 Ensure user is set in the Order
    order = Order.objects.create(
        user=user,  # ✅ Ensure user is stored
        name=name,
        amount=amount,
        provider_order_id=order_id,
        product=product
    )
    order.save()

    return render(request, "user/payment.html", {
        "callback_url": "http://127.0.0.1:8000/razorpay/callback/",  
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "order": order,
        "product": product,
    })



from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.contrib import messages
from .models import Order  # Import your Order model

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    print("POST Data:", request.POST)  # Debugging

    order = None  # Initialize order variable

    if "razorpay_signature" in request.POST:
        provider_order_id = request.POST.get("razorpay_order_id", "")
        payment_id = request.POST.get("razorpay_payment_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        try:
            order = Order.objects.get(provider_order_id=provider_order_id)
            order.payment_id = payment_id
            order.signature_id = signature_id

            print("Order Found:", order)  # Debugging

            if verify_signature(request.POST):
                order.status = "SUCCESS"
                order.save()
                print("Order Updated to SUCCESS")  # Debugging
                messages.success(request, "Payment successful! Your order has been placed.")
            else:
                order.status = "FAILURE"
                order.save()
                print("Signature Verification Failed")  # Debugging
                messages.error(request, "Payment failed. Invalid signature.")
        except Order.DoesNotExist:
            print("Order not found for provider_order_id:", provider_order_id)  # Debugging
            messages.error(request, "Payment failed. Order not found.")

    # Ensure we don't try to access `order.status` if order is None
    return render(request, "callback.html", {"status": order.status if order else "FAILURE"})

from django.db import models
from django.contrib.auth.models import User
# from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus

# Create your models here.

class Register(models.Model):
    Email = models.EmailField(unique=True)
    name = models.TextField()
    phonenumber = models.IntegerField()
    password = models.TextField()
    location= models.TextField()

    def _str_(self):
        return self.name

class Shopreg(models.Model):
    Email = models.EmailField(unique=True)
    name = models.TextField()
    phonenumber = models.IntegerField()
    password = models.TextField()
    location= models.TextField()
    # image = models.FileField()


    def _str_(self):
        return self.name
    
class Category(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    shop = models.ForeignKey(Shopreg,on_delete=models.CASCADE)
    name = models.TextField()
    discription = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.TextField()
    offerprice = models.IntegerField()
    image = models.FileField()

    def _str_(self):
        return self.name +' '+self.shop.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    color = models.CharField(max_length=50)
    sleeve_type = models.CharField(max_length=50)  # Added sleeve type
    image = models.FileField(upload_to="product_images/")

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.sleeve_type}"



class cart(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def _str_(self):
        return self.user.name +' '+self.product.name
    
    def total_price(self):
        return self.quantity * self.product.price
    
class Buy(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_of_buying = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50, null=True, blank=True)  # Store color
    sleeve_type = models.CharField(max_length=50, null=True, blank=True)  # Store sleeve type

    DELIVERY_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("In Transit", "In Transit"),
        ("Delivered", "Delivered"),
    ]
    delivery_status = models.CharField(
        max_length=20, choices=DELIVERY_STATUS_CHOICES, default="Pending"
    )

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.sleeve_type} - {self.delivery_status}"
    


class delivery(models.Model):
    rout = models.TextField()
    Email =  models.EmailField(unique=True)
    password = models.IntegerField()
    name = models.TextField()
    phonenumber = models.IntegerField()
    def __str__(self):
        return self.name




class Feedback(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # Change User to Register
    shop = models.ForeignKey(Shopreg, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.product.name} - {self.rating}★"





# class Order(models.Model):
#     user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True, blank=True)  # Link to user
#     name = models.CharField(max_length=254, blank=False, null=False)
#     amount = models.FloatField(null=False, blank=False)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     status = models.CharField(
#         default=PaymentStatus.PENDING, 
#         max_length=254, 
#         blank=False, 
#         null=False
#     )
#     provider_order_id = models.CharField(max_length=40, null=False, blank=False)
#     payment_id = models.CharField(max_length=36, null=False, blank=False)
#     signature_id = models.CharField(max_length=128, null=False, blank=False)

#     def __str__(self):
#         return f"{self.id} - {self.user.name if self.user else 'Unknown'} - {self.status}"


class Order(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # 🔥 Add this line
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider_order_id = models.CharField(max_length=255, unique=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    signature_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("SUCCESS", "Success"),
            ("FAILURE", "Failure"),
        ],
        default="PENDING",
    )




    


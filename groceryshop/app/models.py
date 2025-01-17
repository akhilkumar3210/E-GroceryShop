from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    category=models.TextField()

class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    descri=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    img=models.FileField()


class Details(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    weight=models.TextField()
    price=models.IntegerField()
    off_price=models.IntegerField()
    stock=models.IntegerField() 

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.ForeignKey(Details, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price=models.FloatField()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.TextField()
    address=models.TextField()
    street=models.TextField()
    city=models.TextField()
    state=models.TextField()
    pincode=models.IntegerField()
    phone=models.IntegerField()

class Buy(models.Model):
    details =models.ForeignKey(Details,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    tot_price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
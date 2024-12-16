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
    weight=models.IntegerField()
    price=models.IntegerField()
    off_price=models.IntegerField()
    stock=models.IntegerField() 
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def gro_login(req):
        if 'shop' in req.session:
                return redirect(shop_home)
        if 'user' in req.session:
                return redirect(user_home)
        if req.method=='POST':
                uname=req.POST['uname']
                password=req.POST['password']
                shop=authenticate(username=uname,password=password)
                if shop:
                        login(req,shop)
                        if shop.is_superuser:
                                req.session['shop']=uname   
                                return redirect(shop_home)
                        else:
                                req.session['user']=uname   
                                return redirect(user_home)
                else:
                        messages.warning(req,'Invaild username or password!!!')
                        return redirect(gro_login)
        else:
                return render(req,'login.html')

def gro_logout(req):
    logout(req)
    req.session.flush()
    return redirect(gro_login)

# ------------------------------------------__Admin--------------------------------------------------------------------------------------------------

def shop_home(req):
    if 'shop' in req.session:
        data=Details.objects.all()
        return render(req,'shop/shop.html',{'data':data})
    else:
        return redirect(gro_login)

def add_product(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['p_id']
            name=req.POST['name']
            descri=req.POST['description']
            categories=req.POST['p_categories']
            img=req.FILES['p_img']
            data=Product.objects.create(pid=pid,name=name,img=img,descri=descri,category=Category.objects.get(category=categories))
            data.save()
            return redirect(details)
        else:
            data=Category.objects.all()        
            return render(req,'shop/addproduct.html',{'data':data})
    else:
        return redirect(gro_login)

def category(req):
    if 'shop' in req.session:
        if req.method == 'POST':
            category=req.POST['p_categories']
            data=Category.objects.create(category=category)
            data.save()
            return redirect(shop_home)
        else:
            data=Category.objects.all()
            return render(req,'shop/category.html',{'data':data})
    else:
         return redirect(gro_login)

def details(req):
    if req.method == 'POST':
            products=req.POST['p_id']
            weight=req.POST['p_weight']
            price=req.POST['p_price']
            offprice=req.POST['of_price']
            stock=req.POST['p_stock']
            data=Details.objects.create(weight=weight,price=price,off_price=offprice,stock=stock,product=Product.objects.get(pid=products))
            data.save()
            return redirect(shop_home)
    else:
            data=Product.objects.all()
            return render(req,'shop/details.html',{'data':data})
    
def edit_product(req,id):
    if req.method=='POST':
        weight=req.POST['p_weight']
        price=req.POST['p_price']
        offprice=req.POST['of_price']
        stock=req.POST['p_stock']
        if weight:
            Details.objects.filter(pk=id).create(weight=weight,price=price,off_price=offprice,stock=stock)
            data=Details.objects.get(pk=id)
            data.weight=weight
            data.save()
        else:
            Details.objects.filter(pk=id).update(weight=weight,price=price,off_price=offprice,stock=stock)
        return redirect(shop_home)
    else:
        data=Details.objects.get(pk=id)
        return render(req,'shop/edit.html',{'data':data})







# ------------------------------------------------user------------------------------------------------------------

def register(req):
    if req.method=='POST':
        email=req.POST['email']
        uname=req.POST['uname']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=password)
            data.save()
            return redirect(gro_login)
        except:
            messages.warning(req,'Email Already Exists!!')
            return redirect(register)
    else:
        return render(req,'user/register.html')
        
def user_home(req):
    if 'user' in req.session:
        product=Product.objects.all()
        return render(req,'user/user.html',{'products':product})
    
     













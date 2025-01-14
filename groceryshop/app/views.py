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
        data=Product.objects.all()  
        data1=Details.objects.all()
        return render(req,'shop/shop.html',{'data':data,'data1':data1})
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

def categoryyy(req):
    if 'shop' in req.session:
        if req.method == 'POST':
            category=req.POST['p_categories']
            data=Category.objects.create(category=category)
            data.save()
            return redirect(categoryyy)
        else:
            data=Category.objects.all()
            return render(req,'shop/category.html',{'data':data})
    else:
         return redirect(gro_login)
    
def delete_cat(req,id):
     data=Category.objects.get(pk=id)
     data.delete()
     return redirect(categoryyy)

def view_category(req,id):
    category = Category.objects.get(pk=id)
    details = Details.objects.filter(product__category=category)
    return render(req, 'shop/view_category.html', {'category': category,'details': details})

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
        pid=req.POST['p_id']
        name=req.POST['name']
        descri=req.POST['description']
        img=req.FILES.get('p_img')
        if img:
            Product.objects.filter(pk=id).update(pid=pid,name=name,descri=descri)
            data=Product.objects.get(pk=id)
            data.img=img
            data.save()
        else:
            Product.objects.filter(pk=id).update(pid=pid,name=name,descri=descri)
        return redirect(shop_home)
    else:
        data=Product.objects.get(pk=id)
        return render(req,'shop/edit.html',{'data':data})
    
def editdetails(req,pid):
    if req.method == 'POST':
        details=req.POST['d_id']
        product=req.POST['p_id']
        weight=req.POST['p_weight']
        price=req.POST['p_price']
        offprice=req.POST['of_price']
        stock=req.POST['p_stock']
        Details.objects.filter(pk=details).update(product=Product.objects.get(pk=product),weight=weight,price=price,off_price=offprice,stock=stock)
        return redirect(shop_home)
    else:      
        data=Details.objects.filter(product=pid)
        data1=Product.objects.get(pk=pid)
        return render(req,'shop/editdetails.html',{'data':data,'data1':data1}) 
    
def deletedetails(req,pid):
     data=Details.objects.get(pk=pid)
     data.delete()
     return redirect(shop_home)

def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)

def bookings(req):
    bookings=Buy.objects.all()[::-1]
    return render(req,'shop/bookings.html',{'bookings':bookings})





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
        data=Details.objects.all()
        data1=Category.objects.all()
        return render(req,'user/user.html',{'products':product,'data':data,'data1':data1})
    
def view_cat(req,id):
    category = Category.objects.get(pk=id)
    details = Details.objects.filter(product__category=category)
    return render(req,'user/view_cat.html', {'category': category,'details': details})
    
def view_pro(req,pid):
    data=Product.objects.get(pk=pid)
    data1=Details.objects.filter(product=pid)
    data2=Details.objects.get(product=pid,pk=data1[0].pk)
    if req.GET.get('dis'):
            dis=req.GET.get('dis')
            data2=Details.objects.get(product=pid,pk=dis)
    return render(req,'user/view_product.html',{'data':data,'data1':data1,'data2':data2})

def add_to_cart(req,id):
    details = Details.objects.get(pk=id)
    user = User.objects.get(username=req.session['user'])
    try:
        cart = Cart.objects.get(details=details, user=user)
        cart.quantity += 1
        cart.save()
    except:
        data = Cart.objects.create(details=details, user=user, quantity=1)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user = User.objects.get(username=req.session['user'])
    data = Cart.objects.filter(user=user)
    return render(req, 'user/cart.html', {'cart': data})

def remove_item(req,id):
    data=Cart.objects.get(pk=id)
    data.delete()
    return redirect(view_cart)

def qty_add(req,cid):
    data=Cart.objects.get(pk=cid)
    if data.details.stock > data.quantity:
        data.quantity+=1
        data.save()
    return redirect(view_cart)

def qty_sub(req,cid):
    data=Cart.objects.get(pk=cid)
    data.quantity-=1
    data.save()
    if data.quantity==0:
        data.delete()
    return redirect(view_cart)

def buyNow(req,pid):
    if 'user' in req.session:
        prod=Details.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if data:
            return redirect("orderSummary",prod=prod.pk,data=data)
        else:
            if req.method=='POST':
                user=User.objects.get(username=req.session['user'])
                name=req.POST['name']
                address=req.POST['address']
                street=req.POST['street']
                city=req.POST['city']
                state=req.POST['state']
                pin=req.POST['pin']
                phone=req.POST['phone']
                data=Address.objects.create(user=user,name=name,address=address,street=street,city=city,state=state,pincode=pin,phone=phone)
                data.save()
                return redirect("orderSummary",prod=prod.pk,data=data)
            else:
                return render(req,"user/address.html")
    else:
        return redirect(gro_login) 
    
def orderSummary(req,prod,data):
    if 'user' in req.session:
        prod=Details.objects.get(pk=prod)
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if req.method == 'POST':
            address=req.POST['address']
            addr=Address.objects.get(user=user,pk=address)
        else:
            return render(req,'user/order.html',{'prod':prod,'data':data})
        print(prod.pk)
        addr=addr.pk
        return redirect("payment",pid=prod.pk,address=addr)   
    else:
        return redirect(gro_login)

def payment(req,pid,address):
    if 'user' in req.session:
        # user=User.objects.get(username=req.session['user'])
        data=Details.objects.get(pk=pid)
        price=data.off_price
        addr=Address.objects.get(pk=address)
        return render(req,'user/payment.html',{'price':price,'data':data,'address':addr})
    else:
        return redirect(gro_login) 

def address(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            phn=req.POST['phn']
            house=req.POST['house']
            street=req.POST['street']
            pin=req.POST['pin']
            state=req.POST['state']
            data=Address.objects.create(user=user,name=name,phn=phn,house=house,street=street,pin=pin,state=state)
            data.save()
            return redirect(address)
        else:
            return render(req,"user/address.html",{'data':data})
    else:
        return redirect(gro_login) 
    

# def address(req,pid):
#      if 'user' in req.session:
#         detail=Details.objects.get(pk=pid)
#         user=User.objects.get(username=req.session['user'])
#         data=Address.objects.filter(user=user)
#         if req.method=='POST':
#             user=User.objects.get(username=req.session['user'])
#             name=req.POST['name']
#             address=req.POST['address']
#             street=req.POST['street']
#             city=req.POST['city']
#             state=req.POST['state']
#             pin=req.POST['pin']
#             phone=req.POST['phone']
#             data=Address.objects.create(user=user,name=name,address=address,street=street,city=city,state=state,pincode=pin,phone=phone)
#             data.save()
#             return redirect('order',detail=detail.pk,data=data)
#         else:
#             return render(req,'user/address.html')

# def order(req,detail):
#     if 'user' in req.session:
#         data1=Details.objects.get(pk=detail)
#         user=User.objects.get(username=req.session['user'])
#         data=Address.objects.filter(user=user)
#         if req.method == 'POST':
#             address=req.POST['address']
#             addr=Address.objects.get(user=user,pk=address)
#         else:
#             return render(req,'user/order.html',{'data1':data1,'data':data}) 
#         print(detail.pk)
#         addr=addr.pk
#         return redirect("payment",pid=detail.pk,address=addr) 
#     else:
#         return redirect(gro_login)


def buy_product(req,pid,address):
    prod=Details.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    quantity=1
    price=prod.off_price
    buy=Buy.objects.create(details=prod,user=user,quantity=quantity,tot_price=price,address=Address.objects.get(pk=address))
    buy.save()
    prod.stock-=1
    prod.save()
    return redirect(user_bookings)

def cart_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    price=cart.quantity*cart.details.off_price
    stock=cart.details.stock-cart.quantity
    
    if stock==0:
        messages.warning(req,'Out of Stock!!!'+cart.details.product.name)
        return redirect(view_cart)
    buy=Buy.objects.create(details=cart.details,user=cart.user,quantity=cart.quantity,tot_price=price)
    buy.save()
    return redirect(user_bookings)



def user_bookings(req):
    user=User.objects.get(username=req.session['user'])
    bookings=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/user_bookings.html',{'bookings':bookings})

def bookings(req):
    bookings=Buy.objects.all()[::-1]
    return render(req,'shop/bookings.html',{'bookings':bookings})
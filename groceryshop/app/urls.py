from django.urls import path
from . import views
urlpatterns=[
    path('',views.gro_login),
    path('logout',views.gro_logout),
    # ----------------------------------------------admin-----------------------------------------------------------------------
    path('shop_home',views.shop_home),
    path('addproduct',views.add_product),
    path('category',views.category),
    path('details',views.details),
    path('edit/<id>',views.edit_product),
    path('delete/<pid>',views.delete_product),


# -----------------------------------------------------------user-----------------------------------------------------------------
    path('register',views.register),
    path('user_home',views.user_home),


]
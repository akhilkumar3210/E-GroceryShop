from django.urls import path
from . import views
urlpatterns=[
    path('',views.gro_login),
    path('logout',views.gro_logout),
    # ----------------------------------------------admin-----------------------------------------------------------------------
    path('shop_home',views.shop_home),
    path('addproduct',views.add_product),
    path('categoryyy',views.categoryyy),
    path('delete_cat/<id>',views.delete_cat),
    path('view_category/<id>',views.view_category),
    path('details',views.details),
    path('edit/<id>',views.edit_product),
    path('delete/<pid>',views.delete_product),
    path('editdetails/<pid>',views.editdetails),
    path('delete_details/<pid>',views.deletedetails),
    path('viewpro/<pid>',views.view_pro),
    path('bookings',views.bookings),




# -----------------------------------------------------------user-----------------------------------------------------------------
    path('register',views.register),
    path('user_home',views.user_home),
    path('add_to_cart/<id>',views.add_to_cart),
    path('cart',views.view_cart),
    path('remove_item/<id>',views.remove_item),
    path('qty_add/<cid>',views.qty_add),
    path('qty_sub/<cid>',views.qty_sub),
    path('view_cat/<id>',views.view_cat),
    path('buynow/<pid>',views.buyNow),
    path('orderSummary/<prod>/<data>',views.orderSummary,name="orderSummary"),
    path('orderSummary2/<cart>',views.orderSummary2,name="orderSummary2"),
    path('payment/<pid>/<address>',views.payment,name="payment"),
    path('address',views.address),
    path('buycart/<cid>',views.carbuy),
    # path('address',views.address),
    path('buy_pro/<pid>/<address>',views.buy_product),
    path('user_book',views.user_bookings,name='userbook'),
    # path('cartbuy/<cid>',views.cart_buy),
    

]
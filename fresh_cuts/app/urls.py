from django.urls import path
from . import views
from .views import callback

urlpatterns = [
    path('',views.login),
    path('logout/',views.logout),
    path('register/',views.register),
    path('shopregister/',views.shopregister),
    path('userhome/',views.userhome,name='userhome'),
    path('adminhome/',views.adminhome),
    # path('shophome',views.shophome),
    path('deliveryhome/',views.deliverys),
    path('addpro/',views.addpro),
    path('viewpro/',views.viewpro),
    # path('shop_view/<int:id>',views.shop_view),
    path('edit/<int:id>',views.edit),
    path('delete/<int:id>',views.delete),
    path('profile/',views.profile),
    # path('viewpro',views.shops),
    path('upload/',views.upload),
    path('category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('userviewproduct/',views.userviewproduct),
    path('prodetails/<int:id>',views.prodetails,name='prodetails'),
    path('shopprodetails/<int:id>',views.shopprodetails),
    path('addtocart/<int:id>',views.user_cart),
    path('user_view_cart/',views.user_view_cart),
    path('qty_incri/<int:id>',views.qty_incri),
    path('qty_decri/<int:id>',views.qty_decri),
    path('buynow1/<int:id>',views.buynow1),
    path('buynow/<int:id>',views.buynow),
    path('deleteitem/<int:id>',views.deleteitem),
    path('orderdetails/',views.orderdetails),
    path('delregister/',views.delregister),
    path('viewshop/',views.viewshop),
    path('aboutus/',views.aboutus),
    path('contact/',views.contact),
    path('service/',views.service),
    path('bookinghistry/',views.bookinghistry),
    path('bookinghistory/',views.bookinghistory),
    path('search/', views.product_search, name='product_search'),
    path('pro_search/', views.pro_search, name='pro_search'),
    path("payment/<int:id>", views.order_payment, name="payment"),
    path("razorpay/callback/", callback, name="razorpay_callback"),  # Ensure the trailing slash
    # path("razorpay/callback/", views.callback, name="callback"),

    # path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    # path('feedback_list/', views.feedback_list, name='feedback_list'),
    # path('admin_feedback/', views.admin_feedback, name='admin_feedback'),

    # path('delivery_home', views.delivery_home, name='delivery_home'),
    # path('order_details/<int:order_id>/', views.view_order_details, name='view_order_details'),
    # path('update_delivery_status/<int:order_id>/<str:new_status>/', views.update_delivery_status, name='update_delivery_status'),
    # path('delivery_history', views.delivery_history, name='delivery_history'),


    

]


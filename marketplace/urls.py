from django.urls import path
from . import views



urlpatterns = [

    path('',views.marketplace,name='marketplace'),
       #cart

    path('cart/',views.cart,name='cart'),

    path('<slug:seller_slug>/', views.seller_detail, name='seller_detail'),

    # ADD TO CART
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    #decrease cART
    path('decrease_cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),

    #delete cart
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),

]
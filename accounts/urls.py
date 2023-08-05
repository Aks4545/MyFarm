from django.urls import path,include
from . import views


urlpatterns = [

    path('',views.MyAccount),
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerSeller/',views.registerSeller,name='registerSeller'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('MyAccount/',views.MyAccount,name='MyAccount'),
    path('custDashboard/',views.custDashboard,name='custDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),

    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    
    
    
    
    path('vendor/',include('seller.urls')),
    path('customers/',include('customers.urls')),

]
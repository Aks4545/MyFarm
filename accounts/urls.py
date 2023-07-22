from django.urls import path
from . import views


urlpatterns = [
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerSeller/',views.registerSeller,name='registerSeller'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('MyAccount/',views.MyAccount,name='MyAccount'),
    path('custDashboard/',views.custDashboard,name='custDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),

]
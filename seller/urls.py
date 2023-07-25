from django.urls import path
from . import views
from accounts import views as AccountViews


urlpatterns = [

    path('',AccountViews.vendorDashboard,name='vendor'),
    path('profile/',views.vprofile,name='vprofile'),
    path('product_add',views.product_add,name='product_add'),
    path('product_add/category/<int:pk>/',views.product_by_category,name='product_by_category'),

    # Category CRUD
    path('product_add/category/add/', views.add_category, name='add_category'),
    path('product_add/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('product_add/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

]
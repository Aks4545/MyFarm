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

    # product crud

    path('product_add/product/add/', views.add_product, name='add_product'),
    path('product_add/product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product_add/product/delete/<int:pk>/', views.delete_product, name='delete_product'),


    #opening hr

        # Opening Hour CRUD
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),

]
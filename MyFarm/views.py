from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request,"home.html")


# def login(request):
#     return render(request,'login.html')

# def register(request):
#     return render(request,'register.html')

# def about(request):
#     return render(request,'about.html')


# def contact(request):
#     return render(request,'contact.html')

# def cart(request):
#     return render(request,'cart.html')


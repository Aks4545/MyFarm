from django.http import HttpResponse
from django.shortcuts import render

from seller.models import seller


def home(request):
    vendors = seller.objects.filter(is_approved=True, user__is_active=True)[:6]
    context={
        'vendors':vendors

    }
    
    return render(request,"home.html",context)




def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')

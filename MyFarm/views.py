from django.http import HttpResponse
from django.shortcuts import  redirect, render
from accounts.forms import contactForm
from django.contrib import messages
from seller.models import seller


def home(request):
    vendors = seller.objects.filter(is_approved=True, user__is_active=True)[:6]
    context={
        'vendors':vendors

    }
    
    return render(request,"home.html",context)




def about(request):
    return render(request,'about.html')


    return contact(request,'contact.html')

def contact(request):

    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
        
            form.save()
            messages.success(request, 'message sent successfully')
            return redirect('contact')
        
        else:
            print('Invalid Form')
            print(form.errors)
    else:
        form = contactForm()    
    context = {
        'form':form,
    }
    
    return render(request,'contact.html',context)
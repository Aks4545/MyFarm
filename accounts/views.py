from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            form.save()
            messages.success(request,'the account has been registered successfully')
            return redirect('registerUser')
        
        else:
            print('Invalid Form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    
    return render(request,'accounts/registerUser.html',context)



















@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
# post_save.connect(post_save_create_profile_receiver, sender=User)



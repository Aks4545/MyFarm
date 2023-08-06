from base64 import urlsafe_b64decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from orders.models import Order
from .utils import detectUser,send_verification_email
from .forms import UserForm
from seller.forms import sellerform
from .models import User,UserProfile
from django.contrib import messages, auth
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from seller.models import seller
from django.template.defaultfilters import slugify
from django.core.mail import EmailMessage

# restrict the vendor from accessing the customerpage

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    


    # restrict the vendor from accessing the customerpage

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('/')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            form.save()
# send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
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




def registerSeller(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('/')
    
    elif request.method == 'POST':
        form=UserForm(request.POST)
        s_form =sellerform(request.POST)
        if form.is_valid() and s_form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.VENDOR
            user.save()
            seller= s_form.save(commit=False)
            seller.user= user
            seller_name = s_form.cleaned_data['seller_name']
            seller.seller_slug = slugify(seller_name)+ '-' + str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            seller.user_profile = user_profile
            seller.save()


            #send verification email

            # mail_subject = 'Please activate your account'
            # email_template = 'accounts/emails/account_verification_email.html'
            # send_verification_email(request, user, mail_subject, email_template)

            messages.success(request,'the account has been registered successfully... please wait for the appproval')
            return redirect('registerSeller')
        else:
            print('invalid form')
    else:
        form = UserForm()
        s_form = sellerform()

    context = {
        'form':form,
        's_form':s_form,
    }
    return render(request,'accounts/registerSeller.html',context)


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_b64decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')



def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('/')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'you are successfully logged in')
            return redirect('MyAccount')
        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')


@login_required(login_url = 'login')
def MyAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)



@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = seller.objects.get(user=request.user)
    return render(request,'accounts/vendorDashboard.html')




@login_required(login_url = 'login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
    }
    return render(request, 'accounts/custDashboard.html', context)





















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



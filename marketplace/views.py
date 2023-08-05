from datetime import date
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from items.models import category,product
from marketplace.models import Cart,Tax
from orders.forms import orderForm
from .context_processors import get_cart_amounts, get_cart_counter
from seller.models import seller,OpeningHour
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from accounts.models import User, UserProfile
# Create your views here.


def marketplace(request):
    vendors = seller.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context={
        'vendors':vendors,
        'vendor_count':vendor_count
    }
    return render (request,'marketplace/listings.html',context)


def seller_detail(request,seller_slug):
    vendor = get_object_or_404(seller,seller_slug=seller_slug)    
    categories = category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('product',
                 queryset=product.objects.filter(is_available=True)
                 )
    )
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', 'from_hour')
    
    # Check current day's opening hours.
    today_date = date.today()
    today = today_date.isoweekday()
    
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
 
    }   
    return render(request,'marketplace/seller_detail.html',context)





def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the  item exists
            try:
                prod = get_object_or_404(product, id=product_id)
                print(prod.id) # <--- must try it
                # Check if the user has already added that item to the cart
                try:
                    print('try to get cart')
                    chkCart, created = Cart.objects.get_or_create(user=request.user, product=prod)
                    print('got the cart')
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    print('cart quantity increased')
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity','qty': chkCart.quantity, 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
                except:
                    print('creating new cart')
                    chkCart, created = Cart.objects.get_or_create(user=request.user, product=prod, quantity = 1)
                    print('cart created')
                    return JsonResponse({'status': 'Success', 'message': 'Added the product to the cart', 'qty': chkCart.quantity, 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                print('This product does not exist!!!')
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

        

    

def decrease_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                prod = get_object_or_404(product, id=product_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = get_object_or_404(Cart, user=request.user, product=prod)
                    if chkCart.quantity > 1:
                        # decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success',  'qty': chkCart.quantity, 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})



#cartview

@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


#delete cart item

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = get_object_or_404(Cart,user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!',  'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})


#seaech viw

def search(request):
    return HttpResponse('search')







@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count= cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    user_profile = get_object_or_404(UserProfile,user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.mobile_no,
        'email': request.user.email,
        'address': user_profile.address,
        # 'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = orderForm(initial=default_values)
    context= {
        'form':form,
        'cart_items':cart_items
    }
    return render(request, 'marketplace/checkout.html',context)



from datetime import date
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render
from items.models import category,product
from marketplace.models import Cart,Tax
from .context_processors import get_cart_counter
from seller.models import seller,OpeningHour
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from accounts.models import User
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
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity})
                except:
                    print('creating new cart')
                    chkCart, created = Cart.objects.get_or_create(user=request.user, product=prod, quantity = 1)
                    print('cart created')
                    return JsonResponse({'status': 'Success', 'message': 'Added the product to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity})
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
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity})
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



#seaech viw

def search(request):
    return HttpResponse('search')







@login_required(login_url='login')
def checkout(request):

    return render(request, 'marketplace/checkout.html')



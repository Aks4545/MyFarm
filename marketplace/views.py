from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render
from items.models import category,product
from marketplace.models import Cart,Tax
from .context_processors import get_cart_counter,get_cart_amounts
from seller.models import seller
from django.db.models import Prefetch

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
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
 
    }   
    return render(request,'marketplace/seller_detail.html',context)



def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the  item exists
            try:
                prod = product.objects.get(product_id)
                # Check if the user has already added that item to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, prod=prod)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, prod=prod, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the product to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})







from django.conf import settings
from django.http import HttpResponse, JsonResponse
import simplejson as json
from django.shortcuts import get_object_or_404, redirect, render
from accounts.utils import send_notification
from items.models import product
from django.contrib.sites.shortcuts import get_current_site
from marketplace.models import Cart, Tax
from marketplace.context_processors import get_cart_amounts
from . forms import orderForm
from .models import Order, Orderedproduct, Payment
from .utils import generate_order_number
import razorpay
from MyFarm.settings import RZP_KEY_ID,RZP_KEY_SECRET


client = razorpay.Client(auth=(settings.RZP_KEY_ID, settings.RZP_KEY_SECRET))
# Create your views here.

def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count= cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    vendors_ids = []
    for i in cart_items:
        if i.product.vendor.id not in vendors_ids:
            vendors_ids.append(i.product.vendor.id)
    
    get_tax = Tax.objects.filter(is_active=True)
    subtotal=0
    total_data = {}
    k = {}
    for i in cart_items:
        prod= get_object_or_404(product,pk= i.product.id,vendor_id__in = vendors_ids)
        v_id= prod.vendor.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += ( prod.price * i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = ( prod.price * i.quantity)
            k[v_id] = subtotal

        # get tax data
        tax_dict= {}
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal)/100, 2)
            tax_dict.update({tax_type: {str(tax_percentage) : str(tax_amount)}})

        # construct total data
        total_data.update({prod.vendor.id:{str(subtotal) : str(tax_dict)}})
    print(total_data)

    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']

    if request.method == 'POST':
        form = orderForm(request.POST)
        if form.is_valid():
            order=Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save() # order id/ pk is generated
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendors_ids)
            order.save()
            # RazorPay Payment
            DATA = {
                "amount": float(order.total) * 100,
                "currency": "INR",
                "receipt": "receipt #"+order.order_number,
                "notes": {
                    "key1": "value3",
                    "key2": "value2"
                }
            }
            rzp_order = client.order.create(data=DATA)
            rzp_order_id = rzp_order['id']

            context = {
                'order': order,
                'cart_items': cart_items,
                'rzp_order_id': rzp_order_id,
                'RZP_KEY_ID': RZP_KEY_ID,
                'rzp_amount': float(order.total) * 100,
            }
            return render(request, 'orders/place_order.html', context)

        else:
            print(form.errors)
    
    return render(request,'orders/place_order.html')\
    

def payments(request):
        # Check if the request is ajax or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # STORE THE PAYMENT DETAILS IN THE PAYMENT MODEL
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()

        # UPDATE THE ORDER MODEL
        order.payment = payment
        order.is_ordered = True
        order.save()

        
        # MOVE THE CART ITEMS TO ORDERED  MODEL
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_product = Orderedproduct()
            ordered_product.order = order
            ordered_product.payment = payment
            ordered_product.user = request.user
            ordered_product.products = item.product
            ordered_product.quantity = item.quantity
            ordered_product.price = item.product.price
            ordered_product.amount = item.product.price * item.quantity # total amount
            ordered_product.save()
        
        # SEND ORDER CONFIRMATION EMAIL TO THE CUSTOMER     
     

        # SEND ORDER RECEIVED EMAIL TO THE VENDOR

       
        # CLEAR THE CART IF THE PAYMENT IS SUCCESS
        cart_items.delete() 

        # RETURN BACK TO AJAX WITH THE STATUS SUCCESS OR FAILURE
        response = {
            'order_number': order_number,
            'transaction_id': transaction_id,
        }
        return JsonResponse(response)    
    return HttpResponse('Payments view')

def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')

    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_prod = Orderedproduct.objects.filter(order=order)

        subtotal = 0
        for item in ordered_prod:
            subtotal += (item.price * item.quantity)

        tax_data = json.loads(order.tax_data)
        print(tax_data)
        context = {
            'order': order,
            'ordered_product': ordered_prod,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }
        return render(request, 'orders/order_complete.html', context)
    except:
        return redirect('home')
from seller.models import seller



def get_vendor(request):
    try:
        vendor = seller.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)
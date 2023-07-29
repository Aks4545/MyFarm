from django.contrib import admin

from  seller.models import OpeningHour, seller

# Register your models here.

class SellerAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'seller_name','is_approved','created_at' )
    list_display_links = ('user','seller_name')
    list_editable = ('is_approved',)


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hour', 'to_hour')

admin.site.register(OpeningHour, OpeningHourAdmin)

admin.site.register(seller,SellerAdmin)
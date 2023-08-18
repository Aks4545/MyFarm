from django.contrib import admin

from  seller.models import OpeningHour, seller

# Register your models here.

class SellerAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'seller_name','is_approved','created_at' )
    list_display_links = ('user','seller_name')
    list_editable = ('is_approved',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hour', 'to_hour')

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return False  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(OpeningHour, OpeningHourAdmin)

admin.site.register(seller,SellerAdmin)
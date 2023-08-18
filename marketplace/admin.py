from django.contrib import admin

from .models import Cart, Tax

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'updated_at')
    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return False  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(Tax, TaxAdmin)
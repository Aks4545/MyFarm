from django.contrib import admin
from .models import Payment,Order,Orderedproduct
# Register your models here.

class OrderedproductAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment', 'user', 'products', 'quantity', 'price', 'created_at']

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return False  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class OrderedProductInline(admin.TabularInline):
    model = Orderedproduct
    readonly_fields = ('payment', 'user', 'products', 'quantity', 'price', 'amount')
    extra = 0

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return False  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, reques, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return True



class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status','order_placed_to', 'is_ordered']
    inlines = [OrderedProductInline]

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return False  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user',  'payment_method', 'amount', 'status','created_at']

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return False  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(Payment,PaymentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Orderedproduct,OrderedproductAdmin)
from django.contrib import admin
from items.models import category,product



# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'updated_at')
    search_fields = ['category_name']

  
    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_title',)}
    list_display = ('product_title', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields = ('product_title', 'category__category_name', 'vendor__vendor_name', 'price')
    list_filter = ('is_available',)
    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(category,CategoryAdmin)
admin.site.register(product,ProductAdmin)
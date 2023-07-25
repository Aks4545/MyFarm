from django.contrib import admin
from items.models import category,product



# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'updated_at')
    search_fields = ['category_name']


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_title',)}
    list_display = ('product_title', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields = ('product_title', 'category__category_name', 'vendor__vendor_name', 'price')
    list_filter = ('is_available',)


admin.site.register(category,CategoryAdmin)
admin.site.register(product,ProductAdmin)
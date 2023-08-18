from django.contrib import admin
from .models import User, UserManager,UserProfile,contact
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','role','is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class userProfileAdmin(admin.ModelAdmin):
    list_display = ('user','city','mobile_no','created_at')

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return False  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
    
class contactAdmin(admin.ModelAdmin):
    list_display = ('name','email','subject','created_at')

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return False  # Prevent superusers from editing
        return True  # Allow staff users to edit

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(contact,contactAdmin)



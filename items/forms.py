from django import forms

from accounts.validators import allow_only_images_validator
from .models import category, product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = ['category_name', 'description']

    
       

class ProductForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = product
        fields = ['category', 'product_title', 'description', 'price', 'image', 'is_available']
       
        
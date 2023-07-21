from django import forms
from .models import seller

class sellerform(forms.ModelForm):
    class Meta:
        model = seller
        fields = ['seller_name']


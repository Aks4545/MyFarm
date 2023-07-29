from django import forms
from .models import OpeningHour, seller

class sellerform(forms.ModelForm):
    class Meta:
        model = seller
        fields = ['seller_name']



class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']
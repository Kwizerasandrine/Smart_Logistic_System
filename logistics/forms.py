from django import forms
from .models import Shipment

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['recipient_name', 'recipient_address', 'recipient_contact', 'weight']
        widgets = {
            'recipient_name': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Full name of recipient',
                'required': True
            }),
            'recipient_address': forms.Textarea(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Full delivery address',
                'rows': 3,
                'required': True
            }),
            'recipient_contact': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': '+234 800 000 0000',
                'type': 'tel',
                'required': True
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': '5.5',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
        }

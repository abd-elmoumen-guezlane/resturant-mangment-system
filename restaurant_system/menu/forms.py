from django import forms
from .models import MenuItem


class AddToCartForm(forms.Form):
    menu_item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'quantity-input',
            'min': '1'
        })
    )


class UpdateCartForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'quantity-input',
            'min': '0'
        })
    )


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Votre nom complet',
            'class': 'form-control'
        })
    )
    customer_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Numéro de téléphone',
            'class': 'form-control'
        })
    )
    customer_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email (optionnel)',
            'class': 'form-control'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Adresse de livraison complète',
            'class': 'form-control',
            'rows': 3
        })
    )
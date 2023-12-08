
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from slice .models import CartItem,UserInformation,Product





class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))




class SecondContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))



class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['old_password'].widget.attrs['placeholder'] = 'Enter current password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter new password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm new password'




class PaymentForm(forms.Form):
    # cartitems = forms.ModelChoiceField(queryset=CartItem.objects.all(), empty_label=None, widget=forms.RadioSelect)
    number = forms.CharField(label='Card Number', max_length=19, widget=forms.TextInput(attrs={'placeholder': 'Enter your card number'}), required=True)
    cvc = forms.CharField(label='CVV', max_length=4, widget=forms.TextInput(attrs={'placeholder': 'Enter CVV'}), required=True)
    expiry = forms.CharField(label='Expiration Date', max_length=7, widget=forms.TextInput(attrs={'placeholder': 'MM/YYYY'}), required=True)
    name = forms.CharField(label='Cardholder Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter cardholder name'}), required=True)





class ProductForm(forms.Form):
    product_type = forms.ModelChoiceField(
        queryset=Product.objects.values_list('type', flat=True).distinct(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
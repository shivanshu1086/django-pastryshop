from django import forms
from django_countries.fields import CountryField


PAYMENT_CHOICES = (
    ('G','Google Pay'),
    ('P','Paytm'),
    ('C','Cash on Delivery')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'1234 Main st'
    }))
    apartment_Address = forms.CharField(required = False,widget=forms.TextInput(attrs={
        'placeholder':'Apartment or suite'
    }))
    country =  CountryField(blank_label='(select country)').formfield(attrs={
        'class':'custom-select d-block w-100'
    })
    zips = forms.IntegerField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    same_address = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

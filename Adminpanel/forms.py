from django import forms
from product.models import Coupon
from django.forms import ModelForm, TextInput,CharField,FloatField,DateTimeField,BooleanField


class AddCoupen(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code','discount','valid_from','valid_to','active']

        widgets = {
            'code': TextInput(attrs={
                'class': "form-control",
                'id':'form5Example1',
                'placeholder' : 'Enter your Coupen code here'

                
                }),
            'discount': TextInput(attrs={
                'class': "form-control",
                'id':'form5Example1',
                'placeholder' : 'Enter your Coupen Discount here'
                
                }),

            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local','class':'form-control','id':'form5Example1','placeholder' : 'Enter your Coupen code here'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local','class':'form-control','id':'form5Example1'}),

           
           
            
        }
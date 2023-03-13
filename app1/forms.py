from django import forms
from django.contrib.auth.models import User
from .models import userprofile,Address
from django.forms import ModelForm, TextInput, EmailInput,NumberInput,ImageField

class updateprofile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                })
        }

class profileupdate(forms.ModelForm):
    class Meta:
        model = userprofile
        fields = ['phone', 'address','postcode','state','city','country','phone2','image','name']

        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                
                }),
            'phone': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                
                }),
            'address': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Address'
                }),
            'postcode': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Postcode'
                }),    
            'state': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'State'
                }),
            'city': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'city'
                }),
            'country': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Country'
                }),
            'phone2': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Alternate Number'
                }),
            
        }



class OrderForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'address','post_code','state','city','country','phone','order_note']

        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                
                }),
            'phone': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                
                }),
            'address': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Address'
                }),
            'post_code': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Postcode'
                }),    
            'state': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'State'
                }),
            'city': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'city'
                }),
            'country': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Country'
                }),
            'order_note': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Alternate Number'
                }),
            
        }
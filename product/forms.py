from django import forms

class CouponForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input','name':'code', 'placeholder': 'Coupon code'}),
    )
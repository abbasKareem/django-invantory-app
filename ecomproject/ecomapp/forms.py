from django import forms
from .models import Order, Product
from django.contrib.auth.models import User


# class CheckoutForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ["ordered_by", "jira_number"]
#         widgets = {
#             'ordered_by': forms.TextInput(attrs={'readonly': 'readonly'}),
#         }

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["jira_number"]
       


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                'Customer with this username already exists.')

        return uname


class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class ProductForm(forms.ModelForm):
    # more_images fields will not save in Product table, so we save it in views.py
    class Meta:
        model = Product
        fields = ["name", "slug", "category", "jira_number", "bar_code", "model"]

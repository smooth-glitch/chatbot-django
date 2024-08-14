from django import forms
from .models import Login, Contact

class LoginModelForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Ensure the password field is rendered as a password input
        }

class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
        }

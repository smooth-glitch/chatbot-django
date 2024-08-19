from django import forms
from .models import *

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


class SignupForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['email', 'password', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        
        return cleaned_data
    
    def save(self, commit=True):
        # Override the save method to handle user creation
        user = super().save(commit=False)
        user.password = self.cleaned_data["password"]  # Assign the cleaned password
        if commit:
            user.save()
        return user

class SetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        email = forms.EmailField(label='Email', max_length=254)
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)


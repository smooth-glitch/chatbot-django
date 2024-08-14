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
            'password': forms.PasswordInput(),  # Use PasswordInput widget for password fields
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
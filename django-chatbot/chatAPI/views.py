from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import Login
from .forms import LoginModelForm, ContactModelForm, SignupForm, ForgotPasswordForm
import pandas as pd
import json
import random
import tensorflow as tf
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .forms import SetPasswordForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .serializers import *

# Load your dataset from a JSON file
df = pd.read_json('mydb.json')
User = get_user_model()
# Load the model
model = tf.keras.models.load_model('trained/chatbot_model.h5')

def preprocess_input(input_text):
    # Example preprocessing step; adjust as needed
    # Ensure this matches the preprocessing used during training
    return input_text.lower().strip()

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            input_text = data.get('patterns', '')

            # Process the input and get the model's prediction
            processed_input = preprocess_input(input_text)
            prediction = model.predict(pd.DataFrame([processed_input], columns=['patterns']))

            # Generate a response using your custom find_response function
            response = find_response(input_text)

            # Get the authenticated user or set to None
            user = request.user if request.user.is_authenticated else None

            # Return the response
            return JsonResponse({'response': response}, status=200)
        except Exception as e:
            # Handle any exceptions and return an error response
            print(f"Error in predict view: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Return an error if the HTTP method is not POST
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

def create_response_dict():
    response_dict = {}
    for _, row in df.iterrows():
        patterns = row['patterns']  # Assume this is already a list
        responses = row['responses']  # Assume this is already a list
        tag = row['tag']
        extra_keys = row.get('extra_keys', {})  # Assume this is already a dictionary

        for pattern in patterns:
            key = pattern.lower()
            if key not in response_dict:
                response_dict[key] = {
                    "responses": responses,
                    "tag": tag,
                    "extra_keys": extra_keys
                }

        # Add tag as a searchable key
        if tag not in response_dict:
            response_dict[tag] = {
                "responses": responses,
                "tag": tag,
                "extra_keys": extra_keys
            }

    return response_dict

response_dict = create_response_dict()

def find_response(user_input):
    user_input = preprocess_input(user_input)
    matched_responses = []

    # Check for exact pattern match
    if user_input in response_dict:
        matched_responses = response_dict[user_input]["responses"]

    # Check for keyword in pattern
    if not matched_responses:
        for key, entry in response_dict.items():
            if any(word in user_input.split() for word in key.split()):
                matched_responses.extend(entry["responses"])

    # Check for tag match
    if not matched_responses:
        for key, entry in response_dict.items():
            if entry["tag"] in user_input:
                matched_responses.extend(entry["responses"])

    if matched_responses:
        return random.choice(matched_responses)
    return "Sorry, I can't help with that. Can you try asking something else?"

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginModelForm
    success_url = reverse_lazy('home')  # Redirect to the home page on successful login

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # Authenticate the user
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            auth_login(self.request, user)  # Log the user in
            messages.success(self.request, "Login successful!")  # Optional: Notify successful login
            return super().form_valid(form)  # Redirect to the success_url (home page)
        else:
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)  # Stay on the same page

    def form_invalid(self, form):
        # Handle the case where the form is invalid
        return self.render_to_response(self.get_context_data(form=form))

    
class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')  # Redirect to the login page after successful signup

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            messages.error(self.request, 'A user with this email already exists.')
            return self.form_invalid(form)
        else:
            # Create a new user with a hashed password
            user = User(username=email, email=email)
            user.set_password(password)  # This hashes the password
            user.save()

            messages.success(self.request, 'Signup successful! Please log in.')
            return redirect('login')

    def form_invalid(self, form):
        # Handle form validation errors
        return self.render_to_response(self.get_context_data(form=form))
    
class ForgotPasswordView(FormView):
    template_name = 'forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        if Login.objects.filter(email=email).exists():
            user = Login.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create password reset URL
            reset_url = self.request.build_absolute_uri(
                reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            # Render email content
            subject = 'Password Reset Requested'
            context = {
                'reset_url': reset_url,
                'user': user,
            }
            html_content = render_to_string('password_reset_email.html', context)
            
            # Send email
            email_message = EmailMultiAlternatives(
                subject,
                html_content,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            
            email_message.send()

            messages.success(self.request, 'A link to reset your password has been sent to your email.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'No user found with this email address.')
            return self.form_invalid(form)
        
    

class PasswordResetConfirmView(FormView):
    template_name = 'password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')
        try:
            uid =force_bytes(urlsafe_base64_decode(uidb64))  # Use force_str instead of force_text
            user = Login.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Login.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Save the new password
            user.set_password(form.cleaned_data['new_password'])
            user.save()

            messages.success(self.request, 'Your password has been successfully reset.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'The reset link is invalid or has expired.')
            return self.form_invalid(form)


@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        form = ContactModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact saved successfully!')
            return redirect('contact')  # Prevent form resubmission
    else:
        form = ContactModelForm()

    return render(request, 'contact.html', {'form': form})
    
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message', '')

            # Debugging: Log the user input
            print(f"User input received: {user_input}")

            response = find_response(user_input)

            # Debugging: Log the generated response
            print(f"Response generated: {response}")

            return JsonResponse({'response': response})
        except Exception as e:
            # Debugging: Log the error
            print(f"Error in chat view: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def chatbot(request):
    return render(request, 'chatbot.html')

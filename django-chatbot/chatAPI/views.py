from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import pandas as pd
import json
import random
import tensorflow as tf

from .forms import (
    CustomUserCreationForm, ContactModelForm, 
    ForgotPasswordForm, SetPasswordForm
)
from .models import ChatHistory


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

            # Save the user's message and chatbot response to the database
            ChatHistory.objects.create(
                user=user,
                user_message=input_text,
                bot_response=response
            )

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
    return "Sorry, I can't help with that. Can you try asking something else?"

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")  # Feedback message
            return redirect('chatbot')  # Redirect to the dashboard or another page
        else:
            # Debugging: Print form errors if the form is not valid
            print(form.errors)
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()
    
    # Include current_page in the context
    return render(request, 'login.html', {'form': form, 'current_page': 'login'})

@api_view(['GET'])
def logout_view(request):
    if request.method == 'GET':
        logout(request)
        # Include current_page in the context
        return render(request, 'logout.html', {'current_page': 'logout'})
    else:
        return Response("Not authorized", status=status.HTTP_401_UNAUTHORIZED)


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signing up
            messages.success(request, "Account created successfully!")  # Feedback message
            return redirect('login')  # Redirect to the dashboard or another page
        else:
            # Debugging: Print form errors if the form is not valid
            print(form.errors)
            messages.error(request, "There was an error creating your account. Please try again.")
    else:
        form = CustomUserCreationForm()

    # Include current_page in the context
    return render(request, 'signup.html', {'form': form, 'current_page': 'signup'})

    
@api_view(['GET', 'POST'])
def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Create password reset URL
                reset_url = request.build_absolute_uri(
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

                messages.success(request, 'A link to reset your password has been sent to your email.')
                return redirect('login')  # Redirect to a success page or home after successful submission
            else:
                messages.error(request, 'No user found with this email address.')
                
        # If the form is invalid or no user is found, re-render the form with errors
        return render(request, 'forgot_password.html', {'form': form})
    
    else:  # GET request
        form = ForgotPasswordForm()
        return render(request, 'forgot_password.html', {'form': form})
        
    
def password_reset_view(request, uidb64=None, token=None):
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            try:
                uid = force_bytes(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                # Save the new password in the auth_user model
                user.set_password(form.cleaned_data['new_password'])
                user.save()

                messages.success(request, 'Your password has been successfully reset.')
                return redirect('login')  # Redirect to the home page or login page
            else:
                messages.error(request, 'The reset link is invalid or has expired.')
                return redirect('password_reset_failed')  # Redirect to an error page
        else:
            # If the form is invalid, re-render the template with form errors
            return render(request, 'password_reset_confirm.html', {'form': form})
    else:  # GET request
        form = SetPasswordForm()
        return render(request, 'password_reset_confirm.html', {'form': form})

@api_view(['GET', 'POST'])
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
@login_required
@api_view(['POST', 'GET'])
def chat(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                # Use request.data provided by DRF to parse JSON data
                data = request.data
                user_input = data.get('message', '')

                # Debugging: Log the user input
                print(f"User input received: {user_input}")

                response = find_response(user_input)

                # Debugging: Log the generated response
                print(f"Response generated: {response}")

                # Get the authenticated user or set to None
                user = request.user if request.user.is_authenticated else None

                # Save the user's message and chatbot response to the database
                ChatHistory.objects.create(
                    user=user,
                    user_message=user_input,
                    bot_response=response
                )

                return JsonResponse({'response': response})
            except Exception as e:
                # Debugging: Log the error
                print(f"Error in chat view: {str(e)}")
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return render(request, 'chatbot.html')
        else:
            return redirect('login')


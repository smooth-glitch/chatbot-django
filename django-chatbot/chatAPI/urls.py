from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # This is your homepage (index.html)
    path('chat/', views.chat, name='chat'),  # This might be another chat-related view
    path('chatbot/', views.chatbot, name='chatbot'),  # New URL pattern for chatbot.html
    path('predict/', views.predict, name='predict'),
    path('login/', views.login_view, name='login'),
    path('contact_us/', views.contact_view, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('reset/<uidb64>/<token>/', views.password_reset_view, name='password_reset_confirm'),
]

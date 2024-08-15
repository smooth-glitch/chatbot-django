from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # This is your homepage (index.html)
    path('chat/', views.chat, name='chat'),  # This might be another chat-related view
    path('chatbot/', views.chatbot, name='chatbot'),  # New URL pattern for chatbot.html
    path('predict/', views.predict, name='predict'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('contact_us/', views.contact_view, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/', views.SignupView.as_view(), name='signup'),
]

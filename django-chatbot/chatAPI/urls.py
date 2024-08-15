from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('chat/', views.chat, name='chat'),  
    path('predict/', views.predict, name='predict'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('contact_us/', views.contact_view, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

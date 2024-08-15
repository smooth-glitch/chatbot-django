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
]

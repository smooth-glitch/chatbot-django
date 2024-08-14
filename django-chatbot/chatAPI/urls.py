from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('chat/', views.chat, name='chat'),  # Make sure this has a trailing slash
    path('predict/', views.predict, name='predict'),
    path('login/', views.login_view, name='login'),
    path('contact_us/', views.contact_view, name='contact'),
    path('about/', views.about, name='about'),
]

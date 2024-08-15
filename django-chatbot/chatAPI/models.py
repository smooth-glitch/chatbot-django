from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

class LoginManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Login(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.IntegerField(null=True, blank=True)

    objects = LoginManager()

    USERNAME_FIELD = 'email'

    def get_email_field_name(self):
        return self.USERNAME_FIELD

    def __str__(self):
        return self.email

    
class Contact(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
"""class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    message = models.TextField()  # The chat message
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the message is created
    is_user_message = models.BooleanField()
    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}'
        """


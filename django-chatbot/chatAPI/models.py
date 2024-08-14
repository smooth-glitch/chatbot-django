from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse

"""class MessageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from user {self.user.username if self.user else 'Unknown'} at {self.timestamp}"
        """


class Login(models.Model):
    email = models.EmailField(max_length = 100, default='test123@gmail.com')
    password = models.CharField(max_length=250)
    phone = models.IntegerField(null = True, blank = True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class Contact(models.Model):
    first_name = models.CharField(max_length=250)
    last_name  = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.IntegerField()

    def __str__(self):
        return self.first_name
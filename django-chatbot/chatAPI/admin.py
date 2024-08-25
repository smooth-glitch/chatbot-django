from django.contrib import admin
from .models import Contact, ChatHistory

# Register your models here.

admin.site.register(ChatHistory)
admin.site.register(Contact)

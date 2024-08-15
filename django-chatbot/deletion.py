import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

# Setup Django
django.setup()
from chatAPI.models import Login
from django.db.models import Count

duplicates = Login.objects.values('email').annotate(email_count=Count('email')).filter(email_count__gt=1)

for duplicate in duplicates:
    Login.objects.filter(email=duplicate['email']).delete()

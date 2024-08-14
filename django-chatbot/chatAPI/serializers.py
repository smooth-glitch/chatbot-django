from rest_framework import serializers
from .models import *
class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = chatHistory 
        fields = '__all__'

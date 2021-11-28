from rest_framework import serializers
from accounts.models import *
from .models import *

class SenderRecieverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'nickname'
        ]

class NoteSerializer(serializers.ModelSerializer):
    sender_id = SenderRecieverSerializer(read_only=True)
    receiver_id = SenderRecieverSerializer(read_only=True)
    class Meta:
        model = Note
        fields = '__all__'
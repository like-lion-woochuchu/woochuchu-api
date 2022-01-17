from rest_framework import serializers
from accounts.models import *
from .models import *
from accounts.models import User


class SenderRecieverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']


class NoteSerializer(serializers.ModelSerializer):
    sender = SenderRecieverSerializer(read_only=True)
    receiver = SenderRecieverSerializer(read_only=True)

    class Meta:
        model = Note
        fields = '__all__'


class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

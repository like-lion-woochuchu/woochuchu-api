from django.db.models import fields
from rest_framework import serializers
from accounts.serializers import AddressSerializer
from .models import *

class FindMyBabyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindMyBabyComment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class FindMyBabySerializer(serializers.ModelSerializer):
    comments = FindMyBabyCommentSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    class Meta:
        model = FindMyBaby
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class FindMyBabyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindMyBaby
        fields = '__all__'
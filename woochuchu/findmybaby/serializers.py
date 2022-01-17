from rest_framework import serializers
from accounts.serializers import AddressSerializer, UserSerializer
from .models import *


class FindMyBabyCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = FindMyBabyComment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class FindMyBabyCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindMyBabyComment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class FindMyBabySerializer(serializers.ModelSerializer):
    comments = FindMyBabyCommentSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = FindMyBaby
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class FindMyBabyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindMyBaby
        fields = '__all__'

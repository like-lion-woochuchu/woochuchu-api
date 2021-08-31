from django.db.models import fields
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'
    

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AddressRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressRegion
        fields = '__all__'


class AddressRoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressRoad
        fields = '__all__'
from rest_framework import serializers
from .models import *

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'

class UserAnimalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnimals
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'profile_img']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class AddressSerializer(serializers.ModelSerializer):
    address_coord_x = serializers.SerializerMethodField()
    address_coord_y = serializers.SerializerMethodField()

    def get_address_coord_x(self, obj):
        return obj.address_coord[0]
    
    def get_address_coord_y(self, obj):
        return obj.address_coord[1]
    class Meta:
        model = Address
        fields = ['address_name', 'address_coord_x', 'address_coord_y']
        read_only_fields = ['created_at', 'updated_at']

class AddressCreateSerializer(serializers.ModelSerializer):
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
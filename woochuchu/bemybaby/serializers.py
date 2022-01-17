from rest_framework import serializers
from .models import BeMyBaby, BeMyBabyComment
from accounts.serializers import AddressSerializer, UserSerializer


class BeMyBabyCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BeMyBabyComment
        fields = '__all__'


class BeMyBabyCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeMyBabyComment
        fields = '__all__'


class BeMyBabySerializer(serializers.ModelSerializer):
    comments = BeMyBabyCommentSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = BeMyBaby
        fields = '__all__'


class BeMyBabyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeMyBaby
        fields = '__all__'

from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import MyBaby, MyBabyComment, MyBabyLike


class MyBabyLikeSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    class Meta:
        model = MyBabyLike
        fields = '__all__'


class MyBabyCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MyBabyComment
        fields = '__all__'


class MyBabyCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBabyComment
        fields = '__all__'


class MyBabySerializer(serializers.ModelSerializer):
    comments = MyBabyCommentSerializer(many=True, read_only=True)
    likes = MyBabyLikeSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = MyBaby
        fields = '__all__'


class MyBabyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBaby
        fields = '__all__'


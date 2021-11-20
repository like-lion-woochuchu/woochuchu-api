from django.db.models.fields.related import ManyToManyField
from rest_framework import serializers

from .models import MyBaby, MyBabyComment, MyBabyLike

class MyBabyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBabyLike
        fields = '__all__'

class MyBabyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBabyComment
        fields = '__all__'


class MyBabySerializer(serializers.ModelSerializer):
    comments = MyBabyCommentSerializer(many=True, read_only=True)
    likes = MyBabyLikeSerializer(many=True, read_only=True)
    class Meta:
        model = MyBaby
        fields = '__all__'



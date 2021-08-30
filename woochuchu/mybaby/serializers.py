from rest_framework import serializers
from .models import MyBaby, MyBabyComment

class MyBabySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBaby
        fields = '__all__'


class MyBabyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBabyComment
        fields = '__all__'
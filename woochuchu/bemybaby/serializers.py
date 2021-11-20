
#파일 이름 serializers 로 바꾸기
from rest_framework import serializers
from .models import BeMyBaby, BeMyBabyComment

class BeMyBabyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeMyBabyComment
        fields = '__all__'

class BeMyBabySerializer(serializers.ModelSerializer):
    comments = BeMyBabyCommentSerializer(many=True, read_only=True)
    class Meta:
        model = BeMyBaby
        fields = '__all__'
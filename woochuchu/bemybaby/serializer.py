from rest_framework import serializers
from .models import BeMyBaby, BeMyBabyComment

class BeMyBabyFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeMyBaby
        fields = '__all__'


class BeMyBabyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeMyBabyComment
        fields = '__all__'

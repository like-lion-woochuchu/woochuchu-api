from django.db.models import fields
from rest_framework import serializers
from .models import *

class FindMyBabySerializer(serializers.ModelSerializer):
    class Meta:
        model = FindMyBaby
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class FindMyBabyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindMyBabyComment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

#파일 이름 serializers 로 바꾸기
from rest_framework import serializers
from .models import BeMyBaby, BeMyBabyComment

class BeMyBabySerializer(serializers.ModelSerializer):
    class Meta:
        model = BeMyBaby
        fields = '__all__'


class BeMyBabyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeMyBabyComment
        fields = '__all__'
        #이거를 field에서 bemybaby를 제외하고 view에서 자동으로 넣어주도록 처리는 불가한가?

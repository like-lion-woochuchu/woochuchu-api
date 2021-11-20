from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import *
from django.db.models import Q
from accounts.permissions import JwtPermission
from rest_framework import status
# Create your views here.

# 쪽지 보내기 -> POST, body => receiver, body
# sender는 JWT에서 추출

# 쪽지 목록

# 쪽지 디테일
class NoteAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_note_objects(self, user_id):
        return Note.objects.filter(Q(sender=user_id) | Q(receiver=user_id))

    def get(self, request):
        try:
            user_id = request.user_id
            notes = self.get_note_objects(user_id)
            serializer = NoteSerializer(notes, many=True)
            data = {
                "results": {
                    "data": serializer.data
                }
            }

            return Response(data=data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)

            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
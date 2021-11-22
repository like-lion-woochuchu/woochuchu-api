from django.core.checks import messages
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import *
from django.db.models import Q
from accounts.permissions import JwtPermission
from rest_framework import status
# Create your views here.

class NotePostAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def post(self, request):
        try:
            request.data['sender'] = request.user_id
            request.data['seen_flag'] = 0
            serializer = NoteSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                data = {
                    "results": {
                        "msg": "데이터가 성공적으로 저장되었습니다."
                    }
                }
            
                return Response(data=data, status=status.HTTP_200_OK)

            else:
                data = {
                    "results": {
                        "msg": serializer.errors,
                        "code": "E4000"
                    }
                }

                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)

            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }


# 현재 JWT user_id와 상대의 user_id 둘 다 사용해서 가져옴
class NoteDetailAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_note_objects(self, subject_id_1, subject_id_2):
        Note.objects.filter(Q(sender=subject_id_1))

# 현재 JWT의 user_id로만 가져옴
class NoteListAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_note_objects(self, user_id, user_uuid):
        try:
            user = User.objects.get(
                id=user_id,
                uuid=user_uuid
                )
        
        except User.DoesNotExist:
            raise PermissionError(
                messages="권한이 없습니다."
                )
        
        return Note.objects.filter(
            Q(sender=user.id) |
            Q(receiver=user.id)
            )

    def get(self, request, user_uuid):
        try:
            notes = self.get_note_objects(request.user_id, user_uuid)
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


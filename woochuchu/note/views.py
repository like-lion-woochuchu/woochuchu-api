from django.core.checks import messages
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer, NoteCreateSerializer
from .models import *
from django.db.models import Q
from accounts.permissions import JwtPermission
from rest_framework import status
# Create your views here.

class NoteGetPostAPIView(APIView):
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
            raise PermissionError
        
        else:
            objects = Note.objects.filter(
                Q(sender=user_id) |
                Q(receiver=user_id)
                ).select_related("receiver", "sender").values(
                    "id", "receiver_id","body", "seen_flag", "created_at"
                ).order_by(
                "-id"
                )

        return objects

    def get(self, request):
        try:
            notes = self.get_note_objects(request.user_id, request.user_uuid)
            serializer = NoteSerializer(notes, many=True)
            data = {
                "results": {
                    "data": serializer.data
                }
            }

            return Response(data=data, status=status.HTTP_200_OK)
        
        except PermissionError:
            data = {
                "results": {
                    "msg": "권한이 없습니다.",
                    "code": "E4010"
                }
            }

            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            print(e)

            data = { 
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            request.data['sender'] = request.user_id
            request.data['seen_flag'] = 0
            serializer = NoteCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "results": {
                        "msg": "쪽지가 성공적으로 발송되었습니다."
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

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NoteDetailAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_note_objects(self, subject_id_1, subject_id_2):
        objects = Note.objects.filter(
            Q(Q(sender=subject_id_1) & Q(receiver=subject_id_2)) |
            Q(Q(sender=subject_id_2) & Q(receiver=subject_id_1))
        ).select_related("receiver", "sender").order_by(
            "id"
        )

        return objects
    
    def get(self, request, receiver_id):
        try:
            notes = self.get_note_objects(request.user_id, receiver_id)
            notes.filter(seen_flag=0).update(seen_flag=1)
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
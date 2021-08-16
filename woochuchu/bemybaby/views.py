from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import serializers, viewsets, generics, mixins
from rest_framework.views import APIView
from .models import BeMyBaby, BeMyBabyComment
from .serializers import BeMyBabyFeedSerializer, BeMyBabyCommentSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
# 피드도 S3 때문에 커스터마이징 위해서 APIView 이용해서 하는 걸로 수정
class BeMyBabyFeedView(APIView):
    def get_objects(self):
        return get_list_or_404(BeMyBaby)

    def get(self, request):
        try :
            bemybaby = self.get_objects()
            serializer = BeMyBabyFeedSerializer(bemybaby, many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND) 

    def post(self, request):
        serializer = BeMyBabyFeedSerializer(data = request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(status = status.HTTP_201_CREATED ) 
        except Exception as e:
            return Response(status= status.HTTP_400_BAD_REQUEST)


class BeMyBabyFeedDetailView(APIView):
    def get_object(self, feed_id):
        return get_object_or_404(BeMyBaby, id = feed_id)

    def get(self, request, feed_id):
        try :
            bemybaby = self.get_object(feed_id)
            serializer = BeMyBabyFeedSerializer(bemybaby)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND) 

    def put(self, request, feed_id):
        try :
            bemybaby = self.get_object(feed_id)
            serializer = BeMyBabyFeedSerializer(bemybaby, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status= status.HTTP_200_OK) 
            else:
                raise ValueError()
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, feed_id):
        try:
            bemybaby = self.get_object(feed_id)
            bemybaby.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


class BeMyBabyCommentAPIView(APIView):
    def get_objects(self, feed_id):
        return get_list_or_404(BeMyBabyComment, bemybaby_id = feed_id)

    def get(self, request, feed_id):
        try:
            comments = self.get_objects(feed_id)
            print(comments)
            serializer = BeMyBabyCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_200_OK)
    
    def post(self, request, feed_id):
        serializer = BeMyBabyCommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_200_OK ) 
        return Response(status= status.HTTP_400_BAD_REQUEST)

class BeMyBabyCommentDetailAPIView(APIView):
    def get_object(self, comment_id):
        return get_object_or_404(BeMyBabyComment, id = comment_id)

    def get(self, request, comment_id):
        try:
            comment = self.get_object(comment_id)
            serializer = BeMyBabyCommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, comment_id):
        try:
            comment = self.get_object(comment_id)
            serializer = BeMyBabyCommentSerializer(comment, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data) 
            else:
                raise ValueError()
        except Exception as e:
            return Response(status= status.HTTP_404_NOT_FOUND)

    def delete(self, request, comment_id):
        try:
            comment = self.get_object(comment_id)
            comment.delete()
            return Response(status = status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
    def get_object(self):
        try:
            return BeMyBaby.objects.all()
        except BeMyBaby.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        bemybaby = self.get_object()
        print(bemybaby)
        if isinstance(bemybaby, Response) :
            return bemybaby
        serializer = BeMyBabyFeedSerializer(bemybaby, many=True)
        return Response(serializer.data) 

    def post(self, request):
        serializer = BeMyBabyFeedSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED ) 
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class BeMyBabyFeedDetailView(APIView):
    def get_object(self, id):
        try:
            return BeMyBaby.objects.get(id = id)
        except BeMyBaby.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        bemybaby = self.get_object(id)
        if isinstance(bemybaby, Response) :
            return bemybaby
        serializer = BeMyBabyFeedSerializer(bemybaby)
        return Response(serializer.data)

    def put(self, request, id):
        bemybaby = self.get_object(id)
        if isinstance(bemybaby, Response) :
            return bemybaby
        serializer = BeMyBabyFeedSerializer(bemybaby, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        bemybaby = self.get_object(id)
        if isinstance(bemybaby, Response) :
            return bemybaby
        bemybaby.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class BeMyBabyCommentAPIView(APIView):
    def get_comments(self, bemybaby_id):
        try:
            return BeMyBabyComment.objects.filter(bemybaby_id = bemybaby_id)
        except BeMyBabyComment.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, bemybaby_id):
        comment = self.get_comments(bemybaby_id)
        print(comment)
        if isinstance(comment, Response):
            return comment
        serializer = BeMyBabyCommentSerializer(comment, many=True)
        return Response(serializer.data)
    
    def post(self, request, bemybaby_id):
        serializer = BeMyBabyCommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED ) 
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class BeMyBabyCommentDetailAPIView(APIView):
    def get_comment(self, id):
        try:
            return BeMyBabyComment.objects.get(id = id)
        except BeMyBabyComment.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT )

    def get(self, request, id):
        comment = self.get_comment(id)
        if isinstance(comment ,Response) :
            return comment
        serializer = BeMyBabyCommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, id):
        comment = self.get_comment(id)
        if isinstance(comment, Response) :
            return comment
        serializer = BeMyBabyCommentSerializer(comment, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        comment = self.get_comment(id)
        if isinstance(comment ,Response) :
            return comment
        comment.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
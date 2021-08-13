from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import serializers, viewsets, generics, mixins
from rest_framework.views import APIView
from .models import BeMyBaby, BeMyBabyComment
from .serializer import BeMyBabyFeedSerializer, BeMyBabyCommentSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class BeMyBabyFeedViewSet(viewsets.ModelViewSet):
    serializer_class = BeMyBabyFeedSerializer
    queryset = BeMyBaby.objects.all()

class BeMyBabyCommentAPIView(APIView):
    def get_comments(self, feed_id):
        return get_list_or_404(BeMyBabyComment, feed_id = feed_id)

    def get(self, request, feed_id):
        comments = self.get_comments(feed_id)
        serializer = BeMyBabyCommentSerializer(comments, many=True)
        return Response(serializer.data) 
    
    def post(self, request, feed_id):
        serializer = BeMyBabyCommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED ) 
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class BeMyBabyCommentDeleteAPIView(APIView):
    def get_comment(self, id):
        return get_object_or_404(BeMyBabyComment, id = id)

    def get(self, request, feed_id, id):
        comment = self.get_comment(id)
        if comment.feed_id == feed_id:
            serializer = BeMyBabyCommentSerializer(comment)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, feed_id, id):
        comment = self.get_comment(id)
        if comment.feed_id == feed_id:
            serializer = BeMyBabyCommentSerializer(comment, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data) 
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, feed_id, id):
        comment = self.get_comment(id)
        if comment.feed_id == feed_id: 
            comment.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        return Response(status= status.HTTP_400_BAD_REQUEST)
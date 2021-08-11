from django.shortcuts import render, get_object_or_404
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
    def get_object(self, id):
        try:
            return BeMyBabyComment.objects.filter(feed_id = id)
        except BeMyBabyComment.DoesNotExist:
            return None
    def get(self, request, id):
        comments = self.get_object(id)
        serializer = BeMyBabyCommentSerializer(comments, many=True)
        return Response(serializer.data)
    def put(self, request, id):
        comments = self.get_object(id)
        serializer = BeMyBabyCommentSerializer(comments, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class BeMyBabyCommentDeleteAPIView(APIView):
    def get_object(self, id):
        try:
            return BeMyBabyComment.objects.get(id = id)
        except BeMyBabyComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND )
    def get(self, request, feed_id, id):
        comment = self.get_object(id)
        serializer = BeMyBabyCommentSerializer(comment)
        return Response(serializer.data)
    def delete(self, request, feed_id, id):
        comment = self.get_object(id)
        comment.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

from django.db.models import query
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, mixins, generics, status
from rest_framework.views import APIView
from .serializers import *
from .models import *

class FindMyBabyViewSet(viewsets.ModelViewSet):
    queryset = FindMyBaby.objects.all()
    serializer_class = FindMyBabySerializer

# 댓글 분리

class FindMyBabyDeletePutAPIView(APIView):
    def get_object(self, feed_id):
        return get_object_or_404(FindMyBaby, id=feed_id)

    def put(self, request, feed_id):
        try:
            feed = self.get_object(feed_id=feed_id)
            serializer = FindMyBabySerializer(feed, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            else:
                raise ValueError("No matched feed")
        
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, feed_id):
        try:
            feed = self.get_object(feed_id=feed_id)
            feed.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FindMyBabyCommentAPIView(APIView):
    def get_objects(self, feed_id):
        return FindMyBabyComment.objects.filter(findmybaby_id=feed_id)
    
    def get(self, request, feed_id):
        comments = self.get_objects
        serializer = FindMyBabyCommentSerializer(comments)
        return Response(serializer.data)
    
    def post(self, request, feed_id):
        serializer = FindMyBabyCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FindMyBabyCommentDeletePutAPIView(APIView):
    def get_object(self, comment_id):
        return get_object_or_404(FindMyBabyComment, id=comment_id)
    
    def delete(self, request, comment_id):
        try:
            comment = self.get_object(comment_id=comment_id)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, commnet_id):
        try:
            comment = self.get_object(comment_id=commnet_id)
            serializer = FindMyBabyCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            else:
                raise serializer.errors
        
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
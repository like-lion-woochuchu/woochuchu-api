from datetime import date
from django.shortcuts import render, get_object_or_404
from requests.api import request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import *
import json
from json.decoder import JSONDecodeError
from accounts.permissions import *
# Create your views here.

class MyBabyAPIView(APIView):
    permission_classes = [
        JwtPermission.IsAuthenticatedOrReadOnly
    ]

    def get_feed_objects(self):
        return MyBaby.objects.all().order_by('-id')

    def get_comment_objects(self, feed_id):
        return MyBabyComment.objects.filter(mybaby_id=feed_id).order_by('id')

    def get(self, request):
        """
        피드를 조회합니다.
        """
        try :
            comment_paired_feeds = []
            feeds = self.get_feed_objects()
            for feed in feeds:
                #피드 본문 처리
                feed_serializer = MyBabySerializer(feed)
                #피드 댓글 처리
                comments = self.get_comment_objects(feed.id)
                comments_count = len(comments)
                comment_serializer = MyBabyCommentSerializer(comments, many=True)
                comment = {
                    "comments_count": comments_count,
                    "comments": comment_serializer.data
                }
                #피드 좋아요 처리
                likes = MyBabyLike.objects.filter(mybaby_id=feed.id)
                likes_count = likes.count()
                data = feed_serializer.data
                likes = {
                    "likes_count": likes_count
                }
                data.update(comment)
                data.update(likes)
                comment_paired_feeds.append(data)
            data = {
                "results": {
                    "data": comment_paired_feeds
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            data = {
                "results":{
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        새 피드를 작성합니다.
        """
        try:
            request.data['user'] = request.user.id
            serializer = MyBabySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "results": {
                        "msg": "데이터가 성공적으로 저장되었습니다."
                    }
                }
                return Response(data=data, status=status.HTTP_200_OK ) 

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

class MyBabyDeletePutView(APIView):
    permission_classes = [
        JwtPermission.IsAuthorUpdateDeleteorReadOnly
    ]

    def get_object(self, feed_id):
        return MyBaby.objects.get(id=feed_id)

    def put(self, request, feed_id):
        try :
            feed = self.get_object(feed_id=feed_id)
            serializer = MyBabySerializer(feed, data=request.data)
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
        except MyBaby.DoesNotExist:
            data = {
                "results": {
                    "msg": "일치하는 데이터가 존재하지 않습니다.",
                    "code": "E4040"
                }
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, feed_id):
        try:
            feed = self.get_object(feed_id=feed_id)
            feed.delete()
            data = {
                "results": {
                    "msg": "데이터가 성공적으로 삭제되었습니다."
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except MyBaby.DoesNotExist:
            data = {
                "results": {
                    "msg": "일치하는 데이터가 존재하지 않습니다.",
                    "code": "E4040"
                }
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MyBabyCommentAPIView(APIView):
    permission_classes = [
        JwtPermission.IsAuthenticatedOrReadOnly
    ]

    def get_objects(self, feed_id):
        return MyBabyComment.objects.filter(mybaby_id=feed_id)
    '''
    def get(self, request, feed_id):
        """
        특정 피드의 댓글들을 조회합니다.
        """
        try:
            comments = self.get_objects(feed_id=feed_id)
            serializer = MyBabyCommentSerializer(comments, many=True)
            data = {
                "results": {
                    "data": serializer.data
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            data={
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    '''
    def post(self, request, feed_id):
        """
        특정 피드에 댓글을 작성합니다.
        """
        try:
            request.data['mybaby'] = feed_id
            request.data['user'] = request.user.id
            serializer = MyBabyCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "results": {
                        "msg": "데이터가 성공적으로 저장되었습니다."
                    }
                }
                return Response(data=data, status=status.HTTP_200_OK ) 

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
            return Response(status=status.HTTP_400_BAD_REQUEST)

class MyBabyCommentDeletePutAPIView(APIView):
    permission_classes = [
        JwtPermission.IsAuthorUpdateDeleteorReadOnly
    ]

    def get_object(self, comment_id):
        return MyBabyComment.objects.get(id=comment_id)

    def put(self, request, comment_id):
        """
        댓글을 수정합니다.
        """
        try:
            comment = self.get_object(comment_id=comment_id)
            serializer = MyBabyCommentSerializer(comment, data=request.data)
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
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, comment_id):
        """
        댓글을 삭제합니다.
        """
        try:
            comment = self.get_object(comment_id=comment_id)
            if request.user.id != comment.user.id:
                data = {
                    "results": {
                        "msg": "권한이 없습니다." 
                    }
                }

                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                comment.delete()
                data = {
                    "results": {
                        "msg": "데이터가 성공적으로 삭제되었습니다."
                    }
                }
                return Response(data=data, status=status.HTTP_200_OK)

        except MyBabyComment.DoesNotExist:
            data = {
                "results": {
                    "msg": "일치하는 데이터가 존재하지 않습니다.",
                    "code": "E4040"
                }
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

class MyBabyLikeAPIView(APIView):
    permission_classes = [
        JwtPermission.IsAuthorUpdateDeleteorReadOnly
    ]

    def get_objects(self, user, feed_id):
        return MyBabyLike.objects.get(mybaby_id=feed_id, user_id=user.id)

    def post(self, request, feed_id):
        try:
            like = self.get_objects(request.user, feed_id)
            like.delete()
            like_count = MyBabyLike.objects.filter(mybaby_id=feed_id).count()
            data = {
                "results": {
                    "data": like_count 
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except MyBabyLike.DoesNotExist:
            MyBabyLike.objects.create(user=request.user, mybaby_id=feed_id)
            like_count = MyBabyLike.objects.filter(mybaby_id=feed_id).count()
            data = {
                "results": {
                    "data": like_count 
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
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
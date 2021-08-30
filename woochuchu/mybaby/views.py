from datetime import date
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import *
import json
from json.decoder import JSONDecodeError
# Create your views here.

class MyBabyAPIView(APIView):
    def get_objects(self):
        return MyBaby.objects.all().order_by('-id')

    def get(self, request):
        try :
            feeds = self.get_objects()
            serializer = MyBabySerializer(feeds, many=True)
            data = {
                "results": {
                    "data": serializer.data
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
        try:
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
            return Response(status=status.HTTP_404_NOT_FOUND)

class MyBabyCommentAPIView(APIView):
    def get_objects(self, feed_id):
        return MyBabyComment.objects.filter(mybaby_id=feed_id)

    def get(self, request, feed_id):
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
    
    def post(self, request, feed_id):
        try:
            request.data['mybaby'] = feed_id
            serializer = MyBabyCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "results": {
                        "msg": "데이터를 성공적으로 저장하였습니다."
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
    def get_object(self, comment_id):
        return MyBabyComment.objects.get(id=comment_id)

    def delete(self, request, comment_id):
        try:
            comment = self.get_object(comment_id=comment_id)
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

    def put(self, request, comment_id):
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


class LikeAPIView(APIView):
    def post(self, request, feed_id):
        try:
            #user = request.user
            if MyBabyLike.objects.filter(user.id=user_id, mybaby_id=feed_id).exists():
                MyBabyLike.objects.filter(user.id=user_id, mybaby_id=feed_id).delete()
            else:
                MyBabyLike.objects.create(user.id=user_id, mybaby_id=feed_id)
                like_count = MyBabyLike.objects.filter(mybaby_id=feed_id).count()
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

    def get(request, feed_id):
        try:
            likes = MyBabyLike.objects.filter(mybaby_id=feed_id)
            likes_count = likes.count()
            data = {
                "results": {
                    "data": likes_count
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
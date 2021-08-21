from datetime import date
import re
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import *

# 피드도 S3 때문에 커스터마이징 위해서 APIView 이용해서 하는 걸로 수정
class BeMyBabyAPIView(APIView):
    def get_objects(self):
        return BeMyBaby.objects.all().order_by('-id')

    def get(self, request):
        try :
            feeds = self.get_objects()
            serializer = BeMyBabySerializer(feeds, many=True)
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
            serializer = BeMyBabySerializer(data=request.data)
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

class BeMyBabyDeletePutView(APIView):
    def get_object(self, feed_id):
        return BeMyBaby.objects.get(id=feed_id)

    def put(self, request, feed_id):
        try :
            feed = self.get_object(feed_id=feed_id)
            serializer = BeMyBabySerializer(feed, data=request.data)
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
        except BeMyBaby.DoesNotExist:
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
        except BeMyBaby.DoesNotExist:
            data = {
                "results": {
                    "msg": "일치하는 데이터가 존재하지 않습니다.",
                    "code": "E4040"
                }
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("e: ", e)
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }
            return Response(status=status.HTTP_404_NOT_FOUND)

class BeMyBabyCommentAPIView(APIView):
    def get_objects(self, feed_id):
        return BeMyBabyComment.objects.filter(bemybaby_id=feed_id)

    def get(self, request, feed_id):
        try:
            comments = self.get_objects(feed_id=feed_id)
            serializer = BeMyBabyCommentSerializer(comments, many=True)
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
            request.data['findmybaby'] = feed_id
            serializer = BeMyBabyCommentSerializer(data=request.data)
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

class BeMyBabyCommentDeletePutAPIView(APIView):
    def get_object(self, comment_id):
        return BeMyBabyComment.objects.get(id=comment_id)

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

        except BeMyBabyComment.DoesNotExist:
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
            serializer = BeMyBabyCommentSerializer(comment, data=request.data)
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


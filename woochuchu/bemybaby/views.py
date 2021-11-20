from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.permissions import *

# 피드도 S3 때문에 커스터마이징 위해서 APIView 이용해서 하는 걸로 수정
class BeMyBabyAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_feed_objects(self):
        return BeMyBaby.objects.all().prefetch_related("comments").order_by('-id')

    def get_comment_objects(self, feed_id):
        return BeMyBabyComment.objects.filter(bemybaby_id=feed_id).order_by('id')

    def get(self, request):
        """
        피드를 조회합니다.
        """
        try :
            feeds = self.get_feed_objects()
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
        """
        새 피드를 작성합니다.
        """
        try:
            request.data['user'] = request.user_id
            request.data['adopt_flag'] = 0
            serializer = BeMyBabySerializer(data=request.data)
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

class BeMyBabyDeletePutView(APIView):
    permission_classes = [
        JwtPermission
    ]
    def get_object(self, feed_id):
        return BeMyBaby.objects.get(id=feed_id)

    def put(self, request, feed_id):
        """
        피드를 수정합니다.
        """
        try :
            feed = self.get_object(feed_id=feed_id)
            if request.user.id != feed.user.id:
                data = {
                    "results": {
                        "msg": "권한이 없습니다." 
                    }
                }

                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

            else:
                request.data['user'] = request.user.id
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
        """
        피드를 삭제합니다.
        """
        try:
            feed = self.get_object(feed_id=feed_id)
            if request.user.id != feed.user.id:
                data = {
                    "results": {
                        "msg": "권한이 없습니다." 
                    }
                }
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            else:
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
            print(e)
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BeMyBabyCommentAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_objects(self, feed_id):
        return BeMyBabyComment.objects.filter(bemybaby_id=feed_id).order_by('id')

    def post(self, request, feed_id):
        """
        특정 피드에 댓글을 작성합니다.
        """
        try:
            request.data['bemybaby'] = feed_id
            request.data['user'] = request.user.id
            serializer = BeMyBabyCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.bemybaby_id = feed_id
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
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BeMyBabyCommentDeletePutAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_object(self, comment_id):
        return BeMyBabyComment.objects.get(id=comment_id)

    def put(self, request, comment_id):
        """
        댓글을 수정합니다.
        """
        try:
            comment = self.get_object(comment_id=comment_id)
            request.data['bemybaby'] = comment.bemybaby_id
            if request.user.id != comment.user.id:
                data = {
                    "results": {
                        "msg": "권한이 없습니다." 
                    }
                }

                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                request.data['user'] = request.user.id
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
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
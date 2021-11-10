from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import *
from accounts.permissions import *
class FindMyBabyAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_feed_objects(self):
        return FindMyBaby.objects.all().prefetch_related("comments").order_by('-id')
    
    def get_comment_objects(self, feed_id):
        return FindMyBabyComment.objects.filter(findmybaby_id=feed_id).order_by('id')

    # 페이지네이션 고려
    # filter 기능 고려 (쿼리스트링 사용 예정)
    def get(self, request):
        try:
            feeds = self.get_feed_objects()
            serializer = FindMyBabySerializer(feeds, many=True)
            data = {
                "results": {
                    "data": serializer.data
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as e:
            # unexpected error
            print(e)
            data = {
                "results": {
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
            serializer = FindMyBabySerializer(data=request.data)
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
            # unexpected error
            print(e)
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FindMyBabyDeletePutAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]
    def get_object(self, feed_id):
        feed = FindMyBaby.objects.get(id=feed_id)
        
        return feed

    def put(self, request, feed_id):
        try:
            feed = self.get_object(feed_id=feed_id)
            if request.user_id != feed.user.id:
                data = {
                    "results": {
                        "msg": "권한이 없습니다." 
                    }
                }

                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

            else:
                request.data['user'] = request.user_id
                serializer = FindMyBabySerializer(feed, data=request.data)
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

        except FindMyBaby.DoesNotExist:
            data = {
                "results": {
                    "msg": "일치하는 데이터가 존재하지 않습니다.",
                    "code": "E4040"
                }
            }

            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # unexpected error
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
            if request.user_id != feed.user.id:
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

        except FindMyBaby.DoesNotExist:
            data = {
                "results": {
                    "msg": "일치하는 데이터가 존재하지 않습니다.",
                    "code": "E4040"
                }
            }

            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # unexpected error
            print(e)
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }

            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

class FindMyBabyCommentAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_objects(self, feed_id):
        return FindMyBabyComment.objects.filter(findmybaby_id=feed_id).order_by('id')

    def get(self, request, feed_id):
        """
        특정 피드의 댓글들을 조회합니다.
        """
        try:
            comments = self.get_objects(feed_id=feed_id)
            serializer = FindMyBabyCommentSerializer(comments, many=True)
            
            data = {
                "results": {
                    "data": serializer.data
                }
            }

            return Response(data=data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # unexpected error
            print(e)
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, feed_id):
        """
        특정 피드에 댓글을 작성합니다.
        """
        try:
            request.data['findmybaby'] = feed_id
            request.data['user'] = request.user_id
            serializer = FindMyBabyCommentSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.findmybaby_id = feed_id
                serializer.save()

                data = {
                    "results": {
                        "msg": "데이터를 성공적으로 저장하였습니다."
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
            # unexpected error
            print(e)
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FindMyBabyCommentDeletePutAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_object(self, comment_id):
        return FindMyBabyComment.objects.get(id=comment_id)

    def put(self, request, comment_id):
        """
        댓글을 수정합니다.
        """
        try:
            comment = self.get_object(comment_id=comment_id)
            request.data['findmybaby'] = comment.findmybaby_id
            if request.user_id != comment.user.id:
                data = {
                    "results": {
                        "msg": "권한이 없습니다." 
                    }
                }

                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                request.data['user'] = request.user_id
                serializer = FindMyBabyCommentSerializer(
                    comment, data=request.data)

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

        except FindMyBabyComment.DoesNotExist:
            data = {
                "results": {
                    "msg": "일치하는 데이터가 존재하지 않습니다.",
                    "code": "E4040"
                }
            }

            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # unexpected error
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
            if request.user_id != comment.user.id:
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

        except FindMyBabyComment.DoesNotExist:
            data = {
                "results": {
                    "msg": "일치하는 데이터가 존재하지 않습니다.",
                    "code": "E4040"
                }
            }

            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # unexpected error
            print(e)
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
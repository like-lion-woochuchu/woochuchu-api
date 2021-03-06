from rest_framework.response import Response
from rest_framework import pagination, status
from rest_framework.views import APIView
from .serializers import *
from .models import *
from accounts.permissions import *
from woochuchu.pagination import PaginationHandlerMixin
from collections import OrderedDict


class BasicPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('feed_count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))


class MyBabyAPIView(APIView, PaginationHandlerMixin):
    permission_classes = [
        JwtPermission
    ]
    pagination_class = BasicPagination

    def get_feed_objects(self):
        return MyBaby.objects.all().select_related("user").prefetch_related("comments", "likes").order_by('-id')

    def get_filtered_feed_objects(self, animals):
        return MyBaby.objects.filter(animal__in=animals).select_related("user").prefetch_related("comments").order_by('-id')

    def get_comment_objects(self, feed_id):
        return MyBabyComment.objects.filter(mybaby_id=feed_id).order_by('id')

    def get(self, request):
        try :
            params = dict(request.query_params)
            feeds = self.get_feed_objects()
            if 'animals_id' in params.keys():
                animals = list(map(int, params['animals_id'][0].split(',')))
                feeds = self.get_filtered_feed_objects(animals)
            page = self.paginate_queryset(feeds)
            if page is not None:
                serializer = self.get_paginated_response(MyBabySerializer(page, many=True).data)
            else:
                serializer = MyBabySerializer(feeds, many=True)

            for feed in serializer.data['data']:
                likes_count, user_like_flag = 0, 0
                liked = feed['likes']
                likes_count = len(liked)
                for like in liked:
                    if like['user'] == request.user_id:
                        user_like_flag = 1
                        break
                del feed['likes']
                feed['likes_count'] = likes_count
                feed['user_like_flag'] = user_like_flag
            data = {
                "results": serializer.data
            }

            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            data = {
                "results":{
                    "msg": "???????????? ????????? ????????????.",
                    "code": "E5000"
                }
            }

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            request.data['user'] = request.user_id
            serializer = MyBabyCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "results": {
                        "msg": "???????????? ??????????????? ?????????????????????."
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
                    "msg": "???????????? ????????? ????????????.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyBabyDeletePutView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_object(self, feed_id):
        return MyBaby.objects.get(id=feed_id)

    def put(self, request, feed_id):
        try :
            feed = self.get_object(feed_id=feed_id)
            if request.user_id != feed.user_id:
                data = {
                    "results": {
                        "msg": "????????? ????????????."
                    }
                }
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

            else:
                request.data['user'] = request.user_id
                serializer = MyBabyCreateSerializer(feed, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        "results": {
                            "msg": "???????????? ??????????????? ?????????????????????."
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
                    "msg": "???????????? ???????????? ???????????? ????????????.",
                    "code": "E4040"
                }
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            data = {
                "results": {
                    "msg": "???????????? ????????? ????????????.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, feed_id):
        try:
            feed = self.get_object(feed_id=feed_id)
            if request.user_id != feed.user_id:
                data = {
                    "results": {
                        "msg": "????????? ????????????." 
                    }
                }

                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

            else:
                feed.delete()
                data = {
                    "results": {
                        "msg": "???????????? ??????????????? ?????????????????????."
                    }
                }

                return Response(data=data, status=status.HTTP_200_OK)

        except MyBaby.DoesNotExist:
            data = {
                "results": {
                    "msg": "???????????? ???????????? ???????????? ????????????.",
                    "code": "E4040"
                }
            }

            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # unexpected error
            print(e)
            data = {
                "results": {
                    "msg": "???????????? ????????? ????????????.",
                    "code": "E5000"
                }
            }

            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyBabyCommentAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_objects(self, feed_id):
        return MyBabyComment.objects.filter(mybaby_id=feed_id).order_by('id')
    
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
            # unexpected error
            print(e)
            data = {
                "results": {
                    "msg": "???????????? ????????? ????????????.",
                    "code": "E5000"
                }
            }

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, feed_id):
        try:
            request.data['mybaby'] = feed_id
            request.data['user'] = request.user_id
            serializer = MyBabyCommentCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.mybaby_id = feed_id
                serializer.save()
                data = {
                    "results": {
                        "msg": "???????????? ??????????????? ?????????????????????."
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
                    "msg": "???????????? ????????? ????????????.",
                    "code": "E5000"
                }
            }
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyBabyCommentDeletePutAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_object(self, comment_id):
        return MyBabyComment.objects.get(id=comment_id)

    def put(self, request, comment_id):
        try:
            comment = self.get_object(comment_id=comment_id)
            request.data['mybaby'] = comment.mybaby_id
            if request.user_id != comment.user_id:
                data = {
                    "results": {
                        "msg": "????????? ????????????." 
                    }
                }

                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

            else:
                request.data['user'] = request.user_id
                serializer = MyBabyCommentCreateSerializer(comment, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        "results": {
                            "msg": "???????????? ??????????????? ?????????????????????."
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
        except MyBabyComment.DoesNotExist:
            data = {
                "results": {
                    "msg": "???????????? ???????????? ???????????? ????????????.",
                    "code": "E4040"
                }
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            data = {
                "results": {
                    "msg": "???????????? ????????? ????????????.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, comment_id):
        try:
            comment = self.get_object(comment_id=comment_id)
            if request.user_id != comment.user_id:
                data = {
                    "results": {
                        "msg": "????????? ????????????." 
                    }
                }

                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                comment.delete()
                data = {
                    "results": {
                        "msg": "???????????? ??????????????? ?????????????????????."
                    }
                }
                return Response(data=data, status=status.HTTP_200_OK)

        except MyBabyComment.DoesNotExist:
            data = {
                "results": {
                    "msg": "???????????? ???????????? ???????????? ????????????.",
                    "code": "E4040"
                }
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            data = {
                "results": {
                    "msg": "???????????? ????????? ????????????.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyBabyLikeAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_objects(self, user_id, feed_id):
        return MyBabyLike.objects.get(mybaby_id=feed_id, user_id=user_id)

    def post(self, request, feed_id):
        try:
            like = self.get_objects(request.user_id, feed_id)
            like.delete()
            data = {
                "results": {
                    "like_flag": 0
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except MyBabyLike.DoesNotExist:
            MyBabyLike.objects.create(user_id=request.user_id, mybaby_id=feed_id)
            data = {
                "results": {
                    "like_flag": 1
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            data = {
                "results": {
                    "msg": "???????????? ????????? ????????????.",
                    "code": "E5000"
                }
            }
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.response import Response
from rest_framework import pagination, status
from rest_framework.views import APIView
from .serializers import *
from .models import *
from accounts.permissions import *
from woochuchu.pagination import PaginationHandlerMixin
from collections import OrderedDict
from accounts.utils import *


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


class FindMyBabyAPIView(APIView, PaginationHandlerMixin):
    permission_classes = [
        JwtPermission
    ]
    pagination_class = BasicPagination

    def get_feed_objects(self):
        return FindMyBaby.objects.all().select_related("address", "user").prefetch_related("comments").order_by('-id')

    def get_filtered_feed_objects(self, animals):
        return FindMyBaby.objects.filter(animal__in=animals).select_related("address", "user").prefetch_related("comments").order_by('-id')
    
    def get_comment_objects(self, feed_id):
        return FindMyBabyComment.objects.filter(findmybaby_id=feed_id).order_by('id')

    def get(self, request):
        try:
            params = dict(request.query_params)
            feeds = self.get_feed_objects()
            if 'animals_id' in params.keys():
                animals = list(map(int, params['animals_id'][0].split(',')))
                feeds = self.get_filtered_feed_objects(animals)
            page = self.paginate_queryset(feeds)
            if page is not None:
                serializer = self.get_paginated_response(FindMyBabySerializer(page, many=True).data)
            else:
                serializer = FindMyBabySerializer(feeds, many=True)
            data = {
                "results": serializer.data
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

    def post(self, request):
        try:
            request.data['user'] = request.user_id
            request.data['find_flag'] = 0
            address_name = request.data["address_name"]
            address_res = get_address(address_name)
            address_exists_id = check_address_exists(address_res)
            
            if address_exists_id:
                request.data['address'] = address_exists_id
                
            else:
                address_id = create_address_data(address_res)
                request.data['address'] = address_id
                
            serializer = FindMyBabyCreateSerializer(data=request.data)
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


class FindMyBabyDetailAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_object(self, feed_id):
        feed = FindMyBaby.objects.select_related("address", "user").prefetch_related("comments").get(id=feed_id)
        
        return feed
    
    def get(self, request, feed_id):
        try:
            feed = self.get_object(feed_id)
            serializer = FindMyBabySerializer(feed)
            data = {
                "results": {
                    "data": serializer.data
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except FindMyBaby.DoesNotExist:
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
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, feed_id):
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
                request.data['user'] = request.user_id
                address_name = request.data["address_name"]
                address_res = get_address(address_name)
                address_exists_id = check_address_exists(address_res)

                if address_exists_id:
                    request.data['address'] = address_exists_id
                
                else:
                    address_id = create_address_data(address_res)
                    request.data['address'] = address_id

                serializer = FindMyBabyCreateSerializer(feed, data=request.data)
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

        except FindMyBaby.DoesNotExist:
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

        except FindMyBaby.DoesNotExist:
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

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FindMyBabyCommentAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_objects(self, feed_id):
        return FindMyBabyComment.objects.filter(findmybaby_id=feed_id).order_by('id')

    def get(self, request, feed_id):
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
                    "msg": "???????????? ????????? ????????????.",
                    "code": "E5000"
                }
            }

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, feed_id):
        try:
            request.data['findmybaby'] = feed_id
            request.data['user'] = request.user_id
            serializer = FindMyBabyCommentCreateSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.findmybaby_id = feed_id
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


class FindMyBabyCommentDeletePutAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def get_object(self, comment_id):
        return FindMyBabyComment.objects.get(id=comment_id)

    def put(self, request, comment_id):
        try:
            comment = self.get_object(comment_id=comment_id)
            request.data['findmybaby'] = comment.findmybaby_id
            if request.user_id != comment.user_id:
                data = {
                    "results": {
                        "msg": "????????? ????????????." 
                    }
                }

                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                request.data['user'] = request.user_id
                serializer = FindMyBabyCommentCreateSerializer(
                    comment, data=request.data)

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

        except FindMyBabyComment.DoesNotExist:
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

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, comment_id):
        try:
            comment = self.get_object(comment_id=comment_id)
            if request.user_id != comment.user.id:
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

        except FindMyBabyComment.DoesNotExist:
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

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

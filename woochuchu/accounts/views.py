from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import *
from .token import *
from rest_framework.decorators import action
import uuid
from .utils import check_address_exists, create_address_data, get_address
from django.db import transaction


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = [
        UserCreateSerializer, UserSerializer, AnimalSerializer, AddressSerializer, AddressRegionSerializer, AddressRoadSerializer
        ]

    @action(methods=['POST'], detail=False)
    def signin(self, request):
        email = request.data['email']
        provider = request.data['provider']

        try:
            user = User.objects.get(
                email=email,
                provider=provider
            )

            payload_value = str(user.uuid) + ":" + str(user.id)
            nickname = user.nickname
            profile_img = user.profile_img

            payload = {
                "subject": payload_value,
                "nickname": nickname,
                "profile_img": profile_img
            }

            access_token = generate_token(payload, "access")

            data = {
                "results": {
                    "access_token": access_token
                }
            }

            return Response(data=data, status=status.HTTP_200_OK)

        except User.DoesNotExist:

            data = {
                "results": {
                    "msg": "유저 정보가 올바르지 않습니다.",
                    "code": "E4010"
                }
            }

            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)

            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        try:
            with transaction.atomic():
                request.data['user']['profile_img'] = config("DEFAULT_PROFILE_IMG")
                user_data = request.data['user']
                user_uuid = str(uuid.uuid4()).replace("-", "")
                user_data['uuid'] = user_uuid
                address_name = request.data["address"]["address_name"]
                address_res = get_address(address_name)
                address_exists_id = check_address_exists(address_res)
                if address_exists_id:
                    user_data['address'] = address_exists_id

                else:
                    address_id = create_address_data(address_res)
                    user_data['address'] = address_id

                # request.data['animals'] : Array of animal ids
                user_data['animals'] = request.data['animals']
                user_serializer = UserCreateSerializer(data=user_data)

                if user_serializer.is_valid():
                    user_serializer.save()

                    user_id = user_serializer.data['id']
                    payload_value = str(user_uuid) + ":" + str(user_id)
                    payload = {
                        "subject": payload_value
                        }
                    access_token = generate_token(payload, "access")

                    data = {
                        "results": {
                            "access_token": access_token
                        }
                    }

                    return Response(data=data, status=status.HTTP_200_OK)

                else:
                    raise ValueError(user_serializer.errors)

        except ValueError as e:

            data = {
                "results": {
                    "msg": e.args,
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

    @action(methods=['POST'], detail=False)
    def token(self, request):
        user_id = request.data['id']
        user_uuid = request.data['uuid']

        try:
            user = User.objects.get(id=user_id, uuid=user_uuid)
            payload_value = str(user_uuid) + ":" + str(user_id)
            payload = {
                "subject": payload_value
            }

            access_token = generate_token(payload, "access")

            data = {
                "results": {
                    "access_token": access_token
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            data = {
                "results": {
                    "msg": "유저 정보가 올바르지 않습니다.",
                    "code": "E4000"
                }
            }

            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

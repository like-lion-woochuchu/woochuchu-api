from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import *
from .token import *
from rest_framework.decorators import action
import uuid
from .utils import get_address
from django.db import transaction
from django.contrib.gis.geos import Point

# refactor
# serializer.errors에 따라 에러메시지 출력하기 (그대로 출력 X)
# 쿼리 최적화하기
# 회원가입 부분 serializer 저장 시 원자성 보장하지 않음

class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = [
        UserSerializer, AnimalSerializer, AddressSerializer, AddressRegionSerializer, AddressRoadSerializer
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
            username = user.username
            profile_img = user.profile_img
            #payload 에 username, userimgurl 포함
            payload = {
                "subject": payload_value,
                "username": username,
                "profile_img": profile_img
            }
            # refresh token 잠시 보류
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
            print(e.message)

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
                user_data = request.data['user']
                user_uuid = str(uuid.uuid4()).replace("-", "")
                user_data['uuid'] = user_uuid

                address_name = request.data['address']['address_name']
                address_name_detail = request.data['address'][
                    'address_name_detail'] if request.data['address']['address_name_detail'] else ""

                try:
                    address_res = get_address(address_name)
                    if address_res['address_type'] == "ROAD_ADDR":
                        address_obj = AddressRoad.objects.get(
                            address_name=address_res['address_name'])

                    elif address_res['address_type'] == "REGION_ADDR":
                        address_obj = AddressRegion.objects.get(
                            address_name=address_res['address_name'])

                    user_data['address'] = address_obj.address_id

                except AddressRoad.DoesNotExist or AddressRegion.DoesNotExist:

                    address_coord = Point(
                        float(address_res["y"]), float(address_res["x"]))

                    address_data = {
                        'address_name': address_res['address_name'],
                        'address_name_detail': address_name_detail,
                        'address_type': address_res['address_type'],
                        'address_coord': address_coord
                    }

                    address_serializer = AddressSerializer(data=address_data)

                    if address_serializer.is_valid():
                        address_serializer.save()

                    else:

                        data = {
                            "results": {
                                "msg": address_serializer.errors,
                                "code": "E4001"
                            }
                        }

                        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

                    address_region_data = {
                        'address': address_serializer.data['id'],
                        'address_name': address_res['address']['address_name'],
                        'region_1depth_name': address_res['address']['region_1depth_name'],
                        'region_2depth_name': address_res['address']['region_2depth_name'],
                        'region_3depth_name': address_res['address']['region_3depth_name'],
                        'region_3depth_h_name': address_res['address']['region_3depth_h_name'],
                        'h_code': address_res['address']['h_code'],
                        'b_code': address_res['address']['b_code'],
                        'mountain_yn': address_res['address']['mountain_yn'],
                        'main_address_no': address_res['address']['main_address_no'],
                        'sub_address_no': address_res['address']['sub_address_no'] if address_res['address']['sub_address_no'] else "",
                        'address_coord': address_coord
                    }

                    address_road_data = {
                        'address': address_serializer.data['id'],
                        'address_name': address_res['road_address']['address_name'],
                        'region_1depth_name': address_res['road_address']['region_1depth_name'],
                        'region_2depth_name': address_res['road_address']['region_2depth_name'],
                        'region_3depth_name': address_res['road_address']['region_3depth_name'],
                        'road_name': address_res['road_address']['road_name'],
                        'underground_yn': address_res['road_address']['underground_yn'] if address_res['road_address']['underground_yn'] else "",
                        'main_building_no': address_res['road_address']['main_building_no'],
                        'sub_building_no': address_res['road_address']['sub_building_no'] if address_res['road_address']['sub_building_no'] else "",
                        'building_name': address_res['road_address']['building_name'] if address_res['road_address']['building_name'] else "",
                        'zone_no': address_res['road_address']['zone_no'],
                        'address_coord': address_coord
                    }

                    address_region_serializer = AddressRegionSerializer(
                        data=address_region_data)
                    address_road_serializer = AddressRoadSerializer(
                        data=address_road_data)
                    
                    if address_region_serializer.is_valid() and address_road_serializer.is_valid():
                        address_region_serializer.save()
                        address_road_serializer.save()
                    
                    else:
                        data = {
                            "results": {
                                "msg": "주소 값이 올바르지 않습니다.",
                                "code": "E4001"
                            }
                        }

                        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

                except Exception as e:
                    print(e)

                # request.data['animals'] : Array of animal ids

                user_data['animals'] = request.data['animals']
                if user_data['address'] is None:
                    user_data['address'] = address_serializer.data['id']
                
                user_serializer = UserSerializer(data=user_data)

                if user_serializer.is_valid():
                    user_serializer.save()

                    user_id = user_serializer.data['id']
                    user_uuid = user_serializer.data['uuid']
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
                    data = {
                        "results": {
                            "msg": user_serializer.errors,
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

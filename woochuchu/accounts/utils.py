import json
from django.db import transaction
import requests
from decouple import config
from .models import *
from django.contrib.gis.geos import Point
from .serializers import *

def get_address(query, analyze_type=None, page=None, size=None):
    # analyze_code = default : similar (일부만 매칭된 값도 반환), possible : exact (정확히 입력한 값에 대하여만 반환)
    # page = 1 ~ 45 (결과 페이지 번호)
    # size = 1 ~ 30 (한 페이지에서 보여질 문서의 갯수)

    url = "https://dapi.kakao.com/v2/local/search/address.json"
    API_KEY = config("KAKAO_API")
    headers = {'Authorization': f'KakaoAK {API_KEY}'}
    params = {"query": query}

    if analyze_type != None:
        params["analyze_type"] = analyze_type

    if page != None:
        params['page'] = page

    if size != None:
        params['size'] = size

    res = requests.get(url, headers=headers, params=params)
    document = json.loads(res.text)
    return document['documents'][0]

# 현재 입력된 주소가 데이터베이스에 존재하는지 확인
def check_address_exists(address_res):
    try:
        if address_res['address_type'] == "ROAD_ADDR":
            address_obj = AddressRoad.objects.get(
            address_name=address_res['address_name'])

        elif address_res['address_type'] == "REGION_ADDR":
            address_obj = AddressRegion.objects.get(
            address_name=address_res['address_name'])
        
        return address_obj.address_id
    
    except AddressRoad.DoesNotExist or AddressRegion.DoesNotExist:
        return False

# 새로운 주소 데이터 생성
def create_address_data(address_res, address_name_detail):
    try:
        with transaction.atomic():
            address_coord = Point(
                float(address_res["y"]), float(address_res["x"])
            )

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
                raise ValueError(address_serializer.errors)

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
                if address_region_serializer.errors:
                    raise ValueError(address_region_serializer.errors)
                
                elif address_road_serializer.errors:
                    raise ValueError(address_road_serializer.errors)
                
                else:
                    raise ValueError("알 수 없는 오류가 발생하였습니다.")

            return address_serializer.data['id']

    except ValueError as e:
        raise e
    
    except Exception as e:
        print(e)
        raise e
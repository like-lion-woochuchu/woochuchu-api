from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.db import transaction

# Create your views here.
import json
import requests
from .models import Address, AddressRegion, AddressRoad


def address(request):
    api_key = "29aa44f6a3ed78c57b872ff27ae9e7e9"
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {'Authorization': f'KakaoAK {api_key}'}
    params = {"query": "서울시 백제고분로 44길 64"}

    res = requests.get(url, headers=headers, params=params)
    document = json.loads(res.text)
    address_res = document['documents'][0]
    print(address_res)

    # 지번주소
    address_name_jibun = address_res['address']['address_name']
    region_1depth_name_jibun = address_res['address']['region_1depth_name']
    region_2depth_name_jibun = address_res['address']['region_2depth_name']
    region_3depth_name_jibun = address_res['address']['region_3depth_name']
    region_3depth_h_name_jibun = address_res['address']['region_3depth_h_name']
    h_code_jibun = address_res['address']['h_code']
    b_code_jibun = address_res['address']['b_code']
    mountain_yn_jibun = address_res['address']['mountain_yn']
    main_address_no_jibun = address_res['address']['main_address_no']
    sub_address_no_jibun = address_res['address']['sub_address_no']
    address_coord_x_jibun = float(address_res['address']['x'])
    address_coord_y_jibun = float(address_res['address']['y'])
    address_coord = Point(address_coord_y_jibun, address_coord_x_jibun)

    # 도로명주소
    address_name_road = address_res['road_address']['address_name']
    region_1depth_name_road = address_res['road_address']['region_1depth_name']
    region_2depth_name_road = address_res['road_address']['region_2depth_name']
    region_3depth_name_road = address_res['road_address']['region_3depth_name']
    road_name_road = address_res['road_address']['road_name']
    underground_yn_road = address_res['road_address']['underground_yn']
    main_building_no_road = address_res['road_address']['main_building_no']
    sub_building_no_road = address_res['road_address']['sub_building_no']
    building_name_road = address_res['road_address']['building_name']
    zone_no_road = address_res['road_address']['zone_no']


    try:
        with transaction.atomic():
            address = Address()
            address.address_name = address_res['address']['address_name']
            address.address_name_detail = "201호"
            address.address_type = address_res['address_type']
            address_coord_x_jibun = float(address_res['address']['x']) 
            address_coord_y_jibun = float(address_res['address']['y']) 
            address_coord = Point(address_coord_y_jibun, address_coord_x_jibun)
            address.address_coord = address_coord
            address.save()

            address_region = AddressRegion()
            address_region.address = address
            address_region.address_name = address_name_jibun
            address_region.region_1depth_name = region_1depth_name_jibun
            address_region.region_2depth_name = region_2depth_name_jibun
            address_region.region_3depth_name = region_3depth_name_jibun
            address_region.region_3depth_h_name = region_3depth_h_name_jibun
            address_region.h_code = h_code_jibun
            address_region.b_code = b_code_jibun
            address_region.mountain_yn = mountain_yn_jibun
            address_region.main_address_no = main_address_no_jibun
            address_region.sub_address_no = sub_address_no_jibun
            address_region.address_coord = address_coord
            address_region.save()

            address_road = AddressRoad()
            address_road.address = address
            address_road.address_name = address_name_road
            address_road.region_1depth_name = region_1depth_name_road
            address_road.region_2depth_name = region_2depth_name_road
            address_road.region_3depth_name = region_3depth_name_road
            address_road.road_name = road_name_road
            address_road.underground_yn_road = underground_yn_road
            address_road.main_building_no = main_building_no_road
            address_road.sub_building_no = sub_building_no_road
            address_road.building_name = building_name_road
            address_road.zone_no = zone_no_road
            address_road.address_coord = address_coord
            address_road.save()
        
    except Exception as e:
        print(e)

def get_address_code(request):
    address = Address.objects.get(id = 1)
    print(address.address_coord)






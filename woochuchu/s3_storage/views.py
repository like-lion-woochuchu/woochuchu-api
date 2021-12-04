from os import stat
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from accounts.permissions import JwtPermission
from .s3_utils import upload_image, delete_image
from rest_framework.response import Response

# Create your views here.
class ImageUploadDeleteAPIView(APIView):
    permission_classes = [
        JwtPermission
    ]

    def post(self, request):
        try:
            file = request.FILES['file']
            img_url = upload_image(file)
            
            data = {
                "results": {
                    "img_url": img_url
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

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            img_urls = request.data['img_url'].split("|")
            for img_url in img_urls:
                delete_image(img_url)

            data = {
                "results": {
                    "msg": "데이터가 정상적으로 삭제되었습니다."
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

            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
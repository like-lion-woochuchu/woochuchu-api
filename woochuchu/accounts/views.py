from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .token import *

def signin(request):
    email = request.data['email']
    provider = request.data['provider']

    try:
        user = User.objects.get(email=email)
        payload_value = user.uuid + ":" + user.id
        
        access_token = generate_token(payload_value, "access")
        refresh_token = generate_token(payload_value, "refresh")

        data = {
            "results": {
                "access_token": access_token,
                "refresh_token": refresh_token
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
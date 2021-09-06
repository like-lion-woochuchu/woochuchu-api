from rest_framework.permissions import BasePermission
from .token import decode_token
from .models import User

# get / post용 permission 
# put / delete용 permission

# 에러 핸들링 - 실패하는 경우 -> 유저가 존재하지 않을 때 / 토큰이 유효하지 않을 때 (토큰 값이 유효하지 않거나  / 토큰이 만료 됐거나) (401)  / Unexpected Error(500)

class JwtPermission(BasePermission):
    def get_jwt(self, request):
        try:
            jwt = request.headers['Authorization']
            jwt = jwt.split("Bearer ")[1]
            jwt = decode_token(jwt)
            token = jwt['subject'].split(":")
            
            """
            token[0] = user_uuid
            token[1] = user_id
            """

            return token
        
        except Exception as e:
            print(e)
            return Exception("Invalid authorization")

    def has_permission(self, request, view):
        try:
            token = self.get_jwt(request)

            user = User.objects.get(
                id=token[1],
                uuid=token[0]
            )

            request.user = user
            return True

        except User.DoesNotExist:
            return False
        
        except Exception as e:
            print(e)
            return False
            # if e.message == "TokenExpiredError: jwt expired":
            #     return False
            
            # elif e.message == "InvalidTokenError: invalid jwt":
            #     return False
            
            # elif e.message == "Invalid authorization":
            #     return False
            
            # else:
            #     print(e)
            #     return False
    
    def has_object_permission(self, request, view, obj):
        try:
            token = self.get_jwt(request)
            decoded = decode_token(token)
            user = User.objects.get(id=obj.user_id)
            
            if decoded['id'] == user.id and decoded['uuid'] == user.uuid:
                return True
            
            else:
                return False

        except Exception as e:
            print(e)
            return False
            # if e.message == "TokenExpiredError: jwt expired":
            #     return False
            
            # elif e.message == "InvalidTokenError: invalid jwt":
            #     return False
            
            # elif e.message == "Invalid authorization":
            #     return False
            
            # else:
            #     print(e)
            #     return False
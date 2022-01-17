from rest_framework.permissions import SAFE_METHODS, BasePermission
from .token import decode_token


def get_jwt(request):
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
        raise Exception("Invalid authorization")


class JwtPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            token = get_jwt(request)
            request.user_id = int(token[1])
            request.user_uuid = token[0]

            return True
        
        except Exception as e:
            print(e)
            data = {
                "results": {
                    "msg": "토큰이 유효하지 않습니다."
                }
            }
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            token = get_jwt(request)
            request.user_id = token[1]
            request.user_uuid = token[0]

            if request.method in SAFE_METHODS:
                return True
        
            else:
                if request.user_id == obj.user.id:
                    return True
        
            return False
        
        except Exception as e:
            print(e)

            return False

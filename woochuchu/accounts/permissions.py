from rest_framework.permissions import BasePermission
from .token import decode_token
from .models import User

class JwtPermission(BasePermission):

    def get_jwt(self, request):
        try:
            jwt = request.headers['Authorization']
            token = jwt.split("Bearer ")[1]

            return token
        
        except:
            return Exception("Invalid authorization")

    def has_permission(self, request, view):
        try:
            token = self.get_jwt(request)
            decoded = decode_token(token)

            User.objects.get(
                id=decoded['id'],
                uuid=decoded['uuid']
            )
            
            return True

        except User.DoesNotExist:
            return False
        
        except Exception as e:
            if e.message == "TokenExpiredError: jwt expired":
                return False
            
            elif e.message == "InvalidTokenError: invalid jwt":
                return False
            
            elif e.message == "Invalid authorization":
                return False
            
            else:
                print(e)
                return False
    
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
            if e.message == "TokenExpiredError: jwt expired":
                return False
            
            elif e.message == "InvalidTokenError: invalid jwt":
                return False
            
            elif e.message == "Invalid authorization":
                return False
            
            else:
                print(e)
                return False
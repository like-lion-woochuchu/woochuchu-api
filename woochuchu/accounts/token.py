import jwt
import datetime
from decouple import config

def generate_token(payload, type):
    if type == "access":
        # 30분
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    elif type == "refresh":
        # 2주
        exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    else:
        raise ValueError("Invalid tokenType")
    
    payload['exp'] = exp
    encoded = jwt.encode(payload, config("SECRET_KEY"), algorithm=config("JWT_ALGORITHM"))

    return encoded

def decode_token(token):
    try:
        decoded = jwt.decode(token, config("SECRET_KEY"), algorithms=config("JWT_ALGORITHM"))
        return decoded
    except jwt.ExpiredSignatureError:
        return "Expired TokenError"
    
    except jwt.InvalidTokenError:
        return "Invalid TokenError"
import jwt
import datetime
from decouple import config


def generate_token(payload, token_type):
    if token_type == "access":
        # 2주
        exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    elif token_type == "refresh":
        # 2주
        exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    else:
        raise Exception("Invalid tokenType")
    
    payload['exp'] = exp
    payload['iat'] = datetime.datetime.utcnow()
    encoded = jwt.encode(payload, config("SECRET_KEY"), algorithm=config("JWT_ALGORITHM"))

    return encoded


def decode_token(token):
    try:
        decoded = jwt.decode(token, config("SECRET_KEY"), algorithms=config("JWT_ALGORITHM"))
        return decoded
    
    except jwt.ExpiredSignatureError:
        raise Exception("TokenExpiredError: jwt expired")
    
    except jwt.InvalidTokenError:
        raise Exception("InvalidTokenError: invalid jwt")
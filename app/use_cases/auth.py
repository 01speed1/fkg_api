import jwt
import datetime
import os

def generate_jwt(data, algorithm='HS256'):
  payload = {
    'data': data,
    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=int( os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
  }

  token = jwt.encode(payload,  os.getenv("SECRET_KEY"), algorithm=algorithm)

  return token

def decode_jwt(token, algorithm='HS256'):
  try:
    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[algorithm])
    return decoded_token
  except jwt.ExpiredSignatureError:
    return None
  except jwt.InvalidTokenError:
    return None
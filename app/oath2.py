from jose import JWTError, jwt
from datetime import datetime, timedelta


SECRETE_KEY = "G8a9BZYitlU5+EPzdIZNcG6gAeo+2QtaNJTm8HfI8XI="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encode_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)

    return encode_jwt

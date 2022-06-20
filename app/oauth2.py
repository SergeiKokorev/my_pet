from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRETE_KEY = "G8a9BZYitlU5+EPzdIZNcG6gAeo+2QtaNJTm8HfI8XI="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encode_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credential_exception):

    try:
        payload = jwt.decode(otken, SECRETE_KEY, algorithm=ALGORITHM)
        id = payload.get("user_id")

        if not id:
            raise credential_exception

        token_data = schemas.TokenData(id=id)
    except JWTError as er:
        raise credential_exception

    
def get_current_user(token: str = Depends(oauth2_scheme)):
    
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNATHORAZED,
        detail="Could not validate credential",
        header={"WWW-Authenticate": "Bearer"}
    )

    return verify_access_token(token, credential_exception)

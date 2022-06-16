from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecate="auto")


def get_hash_password(password):
    return pwd_context(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

from datetime import datetime, timedelta,timezone
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings

def hash_password(password: str)->str:#this function is used to hash the password using bcrypt library and it will be used in the auth.py file while registering the user
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"),salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str,hashed_password: str)->bool:#this function is used to verify the password using bcrypt library and it will be used in the auth,py file while logging in the user
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def create_access_token(data: dict)->str:#this function is used to create the access token using jose library and it will be used in the auth.py file while registering and logging in the user
    to_encode=data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    token = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return token

def verify_token(token:str)->Optional[dict]:#this function is used to verify the token using jose library and it will be used in the dependencies.py
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
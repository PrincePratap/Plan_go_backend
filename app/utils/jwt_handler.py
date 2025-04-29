from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "29f8fdcbb43b484c8b17b69d8e24ebea2df9c7e4f8c0325d14c9c4c4a9df3a6b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

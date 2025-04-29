from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate
from passlib.context import CryptContext
from app.utils.jwt_handler import create_access_token


auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

@auth_router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

     # generate token
    access_token = create_access_token(data={"sub": new_user.email})
    
    return {
        "msg": "User registered successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }
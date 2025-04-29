from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    
class UserLogin(BaseModel):
    email: str
    password: str

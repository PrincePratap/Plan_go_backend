from pydantic import BaseModel, EmailStr


class UserDynamoCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    phone_number: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


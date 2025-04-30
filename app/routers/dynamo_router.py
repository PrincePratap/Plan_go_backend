from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserDynamoCreate, UserLogin
from app.utils.jwt_handler import create_access_token
import boto3
import uuid
from passlib.context import CryptContext

# Setup
dynamo_router = APIRouter()
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Users")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Check if user exists
def is_user_exist(email: str, phone_number: str):
    response = table.scan(
        FilterExpression="email = :e OR phone_number = :p",
        ExpressionAttributeValues={":e": email, ":p": phone_number}
    )
    return response["Count"] > 0

# Add user
def add_user(user_data: dict):
    user_id = str(uuid.uuid4())
    item = {"id": user_id, **user_data}
    table.put_item(Item=item)
    return item

# Register
@dynamo_router.post("/register")
def register_user_dynamo(user: UserDynamoCreate):
    if is_user_exist(user.email, user.phone_number):
        raise HTTPException(status_code=400, detail="Email or Phone Number already registered")

    user_data = user.dict()
    user_data["password"] = hash_password(user.password)
    saved = add_user(user_data)

    access_token = create_access_token(data={"sub": saved["email"]})
    return {
        "msg": "User saved to DynamoDB",
        "user": saved,
        "access_token": access_token,
        "token_type": "bearer"
    }

# Login
@dynamo_router.post("/login")
def login_user(user: UserLogin):
    response = table.scan(
        FilterExpression="email = :e",
        ExpressionAttributeValues={":e": user.email}
    )
    if response["Count"] == 0:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db_user = response["Items"][0]

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user["email"]})
    return {
        "msg": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }

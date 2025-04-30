import boto3
import uuid

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")  # confirm region

def add_user(data: dict):
    data["id"] = str(uuid.uuid4())
    print("📦 Saving user data:", data)  # Debug print

    table = dynamodb.Table("Users")
    response = table.put_item(Item=data)
    print("✅ DynamoDB response:", response)  # Debug print

    return data
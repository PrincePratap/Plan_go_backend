from fastapi import FastAPI
from app.routers import  dynamo_router
# from app.database import engine, Base

# Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(auth_router.auth_router)
app.include_router(dynamo_router.dynamo_router)  # ✅ Must be included

from fastapi import FastAPI
from app.routers import auth_router
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router.auth_router)




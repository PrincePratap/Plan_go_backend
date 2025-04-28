from fastapi import FastAPI
from app.routers import auth_router
from app.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(auth_router.router)

@app.get("/")
def homepage():
    return {"message": "Welcome to PlanGo Backend API!"}

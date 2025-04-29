from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Your Database URL
DATABASE_URL = "mysql+pymysql://root:cody2002@localhost/plango_db"

# Create Engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base Class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

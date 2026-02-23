from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from pathlib import Path
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() 

# Resolve credentials file from the project root regardless of current working directory.
credentials_path = Path(__file__).resolve().parents[2] / "credentials.json"
with credentials_path.open("r", encoding="utf-8") as credentials_txt:
    credentials = json.loads(credentials_txt.read())

engine = create_engine(credentials["db_connections"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

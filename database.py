from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json


with open("credentials.json", "r", encoding="utf-8") as credentials_txt:
    credentials = json.loads(credentials_txt.read())

engine = create_engine(credentials["db_connections"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
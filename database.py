from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json


credentials_txt = open("credentials.json", "r")

credentials = json.loads(credentials_txt.read())

engine = create_engine(credentials["db_connections"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from passlib.context import CryptContext
from database.database import credentials


pwd_context = CryptContext(schemes=[credentials["schemes"]], deprecated="auto")

def hash_password(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    password = password[:72]
    return pwd_context.verify(password, hashed_password)

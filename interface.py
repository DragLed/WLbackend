from sqlalchemy import text
from database import engine  
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


class DataBaseInterface:

    @staticmethod
    def create_gift(name, description, price, photo):
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO gifts (name, description, price, photo) VALUES (:n, :d, :p, :ph)"),
                {"n":name,"d":description,"p":price,"ph":photo}
            )

    @staticmethod
    def get_all_gifts():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM gifts"))
            return [dict(row._mapping) for row in result]
    
    @staticmethod
    def delete_gift(id):
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM gifts WHERE id = :id"),
                {"id": id}
            )

    @staticmethod
    def get_gift_by_id(id):
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM gifts WHERE id = :id"),
                {"id": id}
            ).fetchone()  
            return dict(result._mapping) if result else None
    
    @staticmethod
    def edit_gift_by_id(id, name, description, price, photo):
        with engine.begin() as conn:
            conn.execute(
                text("""UPDATE gifts SET name = :n,
                                        description = :d,
                                    price = :p,
                                    photo = :ph
                                    WHERE id = :id"""),
                {"n":name,"d":description,"p":price,"ph":photo,"id": id}
            )

    

    @staticmethod
    def create_user(login:str, email: str,password:str):
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (login,email,hashed_password) VALUES (:l,:e, :ps)"),
                {"l": login, "e": email, "ps": hash_password(password)}
            )


    @staticmethod
    def get_all_users():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users"))
            return [dict(row._mapping) for row in result]


    @staticmethod
    def get_user_by_email(email: str):
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE email = :e"),
                {"e": email}
            ).fetchone() 
            return dict(result._mapping) if result else None

    @staticmethod
    def get_user_by_login(login: str):
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE login = :l"),
                {"l": login}
            ).fetchone() 
            

    @staticmethod
    def verify_password_by_login(login:str,password: str):
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE login = :l"),
                {"l": login}
            ).fetchone()
            result = dict(result._mapping) if result else None
            p = verify_password(password, result["hashed_password"])
            if p:
                return True
            return False
        
    @staticmethod
    def verify_password_by_email(email:str,password: str):
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE email = :l"),
                {"l": email}
            ).fetchone()
            result = dict(result._mapping) if result else None
            p = verify_password(password, result["hashed_password"])
            if p:
                return True
            return False


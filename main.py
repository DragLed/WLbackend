from fastapi import FastAPI, HTTPException
from interface import DataBaseInterface
from fastapi.middleware.cors import CORSMiddleware
from models import Base
from database import engine
import uvicorn

Base.metadata.create_all(bind=engine)
print("Таблицы созданы")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/new_gift")
def create_gift(name: str, description: str, price: float, photo: str = None):
    DataBaseInterface.create_gift(name, description, price, photo)
    return {"message": "Подарок дабавлен"}


@app.get("/all_gifts")
def get_all_gifts():
    gifts = DataBaseInterface.get_all_gifts()
    return gifts

@app.delete("/delete_gift")
def remove_gift(gift_id: int):
    DataBaseInterface.delete_gift(gift_id)
    return {"message": "Подарок удалён"}

@app.get("/gift_by_id")
def get_gift_by_id(gift_id: int):
    gift = DataBaseInterface.get_gift_by_id(gift_id)
    if gift:
        return gift
    return {"error": "Подарок не найден"}


@app.put("/edit_gift_by_id")
def edit_gift_by_id(id: int, name: str, description: str, price: float, photo: str = None):
    gift = DataBaseInterface.get_gift_by_id(id)
    if gift:
        DataBaseInterface.edit_gift_by_id(id ,name, description, price, photo)
        return {"message": f"Подарок с id: {id} обновлён"}
    else:
        return {"message": f"Подарок с id: {id} не найден"}
    
@app.post("/register")
def create_user(login:str, email: str, password: str):
    user = DataBaseInterface.get_user_by_email(email)
    if user:
        raise HTTPException(status_code=400, detail="Email уже используется")
    user = DataBaseInterface.get_user_by_login(login)
    if user:
        raise HTTPException(status_code=400, detail="login уже используется")
    DataBaseInterface.create_user(login, email, password)
    return {"login": login,"email": email, "message": "Пользователь создан"}

@app.get("/get_all_users")
def get_all_users():
    result = DataBaseInterface.get_all_users()
    return result


@app.get("/get_user_by_email")
def get_user_by_email(email:str):
    result = DataBaseInterface.get_user_by_email(email)
    return result

@app.get("/get_user_by_login")
def get_user_by_login(login:str):
    result = DataBaseInterface.get_user_by_login(login)
    return result


@app.get("/verify_password_by_login")
def verify_password_by_login(login:str, password: str):
    return DataBaseInterface.verify_password_by_login(login, password)

@app.get("/verify_password_by_email")
def verify_password_by_email(email:str, password: str):
    return DataBaseInterface.verify_password_by_email(email, password)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
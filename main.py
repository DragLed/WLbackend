from fastapi import FastAPI
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
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
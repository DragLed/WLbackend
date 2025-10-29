from sqlalchemy import text
from database import engine  

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
            ).fetchone()  # Получаем одну строку (подарок)
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

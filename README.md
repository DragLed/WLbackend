# WLbackend — Backend для Wishlist App

## 🚀 О проекте
WLbackend — серверная часть приложения Wishlist App (список желаний).  
Приложение позволяет пользователям создавать собственные wishlists, добавлять элементы, делиться ими и работать совместно с другими пользователями.

Бэкенд написан на **Python + FastAPI**, использует **JWT‑аутентификацию**, REST API и подключение к базе данных (PostgreSQL).

---

## 🧩 Основные возможности
- Регистрация и авторизация пользователей (JWT)
- CRUD для списков желаний (создание / просмотр / редактирование / удаление)
- CRUD для элементов внутри списка (например: название, цена, описание, фото)
- Возможность совместного доступа к списку (share)
- Автоматически генерируемая API‑документация Swagger / Redoc

---

## 🔧 Технологии
| Компонент          | Используемые технологии |
|-------------------|--------------------------|
| Backend Framework | FastAPI                  |
| Язык              | Python 3.11+            |
| База данных       | PostgreSQL              |
| ORM/DB Layer      | SQLAlchemy              |
| Авторизация       | OAuth2 + JWT            |
| Документация API  | Swagger / Redoc         |

---

## 📂 Структура проекта
```
WLbackend/
│── main.py          # Точка входа FastAPI
│── models.py        # Модели БД (User, Wishlist, Item)
│── interface.py     # Логика обработки/сервисы
│── database.py      # Подключение к БД, session
│── requirements.txt # Список зависимостей
│── README.md        # Документация проекта
```

---

## ✅ Запуск проекта

### 1. Клонируй репозиторий
```sh
git clone https://github.com/DragLed/WLbackend.git
cd WLbackend
```

### 2. Создай виртуальное окружение
```sh
python -m venv venv
source venv/bin/activate  # Linux / MacOS
venv\Scripts\activate   # Windows
```

### 3. Установи зависимости
```sh
pip install -r requirements.txt
```

### 4. Запусти сервер
```sh
uvicorn main:app --reload
```

### 5. Открой документацию API

Swagger:
```
http://localhost:8000/docs
```

Redoc:
```
http://localhost:8000/redoc
```

---

## 🧪 Пример API запросов

### 🔹 Регистрация
`POST /auth/register`
```json
{
  "email": "example@mail.com",
  "login": "my_login",
  "password": "123456"
}
```

### 🔹 Авторизация (получение JWT)
`POST /auth/login`
```json
{
  "login": "my_login",
  "password": "123456"
}
```

### 🔹 Создание wishlist
`POST /wishlists`
```json
{
  "name": "Подарки на ДР",
  "description": "Список желаемого на день рождения"
}
```

---

## 🛠 План улучшений
- Docker + docker-compose для автоматического деплоя
- Логирование и мониторинг
- Система ролей и разрешений (чтение / редактирование / владелец)
- Уведомления (email + push в будущем)

---

## 👨‍💻 Автор
**Корниенко Никита (DragLed)** — full‑stack разработчик, создаёт Wishlist App как pet‑project и как учебный full‑stack продукт.

---

## 📄 Лицензия
Проект распространяется под лицензией **MIT**.

---

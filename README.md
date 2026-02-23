# WLbackend

Backend API for a wishlist application, built with FastAPI, SQLAlchemy, and JWT (cookie-based auth).

## Features
- User registration and login.
- Authentication via JWT stored in HttpOnly cookie (`my_access_token`).
- CRUD for wishlists.
- CRUD for gifts inside wishlists.
- Basic developer endpoints (`/dev/*`) for health and stats.
- Swagger and ReDoc documentation out of the box.

## Tech Stack
- Python 3.12 (recommended)
- FastAPI
- SQLAlchemy
- PostgreSQL (`psycopg2`)
- AuthX (JWT)
- Alembic

## Project Structure
```text
WLbackend/
  src/
    main.py
    api/
    config/
    core/
    database/
    models/
    router/
    schemas/
    alembic/
    alembic.ini
  requirements.txt
  dockerfile
  credentials.json
```

## Configuration
The app reads settings from `credentials.json` in the project root.

Required keys:
```json
{
  "db_connections": "postgresql+psycopg2://USER:PASSWORD@HOST:5432/DB_NAME",
  "JWT_SECRET_KEY": "your_secret_key",
  "schemes": "your scheme"
}
```

## Local Run
1. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Apply migrations:
```bash
cd src
alembic -c alembic.ini upgrade head
cd ..
```

4. Start API:
```bash
cd src
uvicorn main:app --reload
```

API will be available at `http://127.0.0.1:8000`.

## Docker
Build image:
```bash
docker build -t wlbackend -f dockerfile .
```

Run container:
```bash
docker run --rm -p 8000:8000 wlbackend
```

## API Docs
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Auth Flow
1. Register user via `POST /auth/`.
2. Login via `POST /auth/login`.
3. After login, server sets HttpOnly cookie `my_access_token`.
4. Use protected endpoints with this cookie attached.

## Main Endpoints

### Auth
- `POST /auth/` - register user
- `POST /auth/login` - login and set auth cookie
- `POST /auth/logout` - clear auth cookie (protected)
- `POST /auth/reset_password` - change password (protected)
- `GET /auth/me` - get current user (protected)

### Users
- `GET /users/` - list users
- `GET /users/{Id}` - get user by id
- `DELETE /users/{Id}` - delete own user and clear cookie (protected)
- `GET /users/{userId}/wishlist` - get user wishlists (protected)

### Wishlist
- `POST /wishlist/` - create wishlist (protected)
- `GET /wishlist/` - get current user wishlists (protected)
- `GET /wishlist/{id}` - get wishlist by id (protected)
- `DELETE /wishlist/{id}` - delete wishlist (protected)

### Gifts
- `POST /gifts/` - create gift (protected)
- `GET /gifts/{gift_id}` - get gift by id (protected)
- `DELETE /gifts/{giftId}` - delete gift (protected)
- `GET /gifts/{wishlist_id}/wishlist` - list gifts in wishlist (protected)

### Dev
- `GET /dev/health` - DB health check (protected)
- `GET /dev/stats` - users/gifts stats (protected)
- `GET /dev/wishlist` - all wishlists (protected)

## Notes
- CORS is preconfigured for:
  - `http://localhost:5173`
  - `http://127.0.0.1:5173`
  - `https://dragledwl.ru`
- Entry point for local development is `src/main.py`.

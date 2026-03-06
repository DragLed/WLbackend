# WLbackend

FastAPI backend for a shared wishlist application.

It supports:
- user registration and login
- cookie-based JWT authentication
- wishlist management with visibility rules
- per-user access roles for shared wishlists (`viewer` / `editor`)
- gift management inside wishlists

## Tech Stack
- Python 3.11+
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Alembic
- AuthX (JWT in cookies)

## Project Layout
```text
WLbackend/
|-- src/
|   |-- api/          # business logic
|   |-- router/       # HTTP endpoints
|   |-- models/       # SQLAlchemy models
|   |-- schemas/      # Pydantic schemas
|   |-- database/     # DB engine/session setup
|   |-- config/       # auth and security config
|   |-- core/         # enums and shared constants
|   |-- alembic/      # migrations
|   |-- alembic.ini
|   `-- main.py       # app entry point
|-- requirements.txt
`-- credentials.json
```

## Configuration
The app reads config from `credentials.json` in the project root.

Example:
```json
{
  "db_connections": "postgresql+psycopg2://USER:PASSWORD@HOST:5432/DB_NAME",
  "JWT_SECRET_KEY": "replace_with_strong_secret",
  "schemes": "argon2"
}
```

- `db_connections`: SQLAlchemy database URL
- `JWT_SECRET_KEY`: secret used to sign JWT tokens
- `schemes`: passlib hashing scheme (for example `argon2` or `bcrypt`)

## Local Setup
1. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
cd src
alembic -c alembic.ini upgrade head
```

4. Start the API:
```bash
uvicorn main:app --reload
```

API base URL: `http://127.0.0.1:8000`

## API Documentation
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Authentication Flow
1. Register: `POST /auth/register/`
2. Login: `POST /auth/login`
3. Server sets HttpOnly cookie: `my_access_token`
4. Call protected routes with that cookie
5. Logout: `PATCH /auth/logout`

## Access Model
Wishlist visibility values:
- `public`
- `link_only`
- `private`

Access roles for shared wishlists:
- `viewer`
- `editor`

Owners always have full access to their own wishlists.

## Endpoints Overview

### Auth
- `POST /auth/register/` - register user
- `POST /auth/login` - login and set auth cookie
- `PATCH /auth/logout` - logout and clear auth cookie (auth required)
- `POST /auth/password` - change password (auth required)
- `GET /auth/me` - current user profile (auth required)

### Users
- `GET /users/` - list users
- `GET /users/{Id}` - user by id
- `GET /users/search/{username}?q=<prefix>` - search users by username prefix (auth required)
- `DELETE /users/{Id}` - delete own account (auth required)
- `GET /users/{userId}/wishlist` - wishlists by user id (auth required)

### Wishlist
- `POST /wishlist/?visibility=<public|link_only|private>` - create wishlist (auth required)
- `GET /wishlist/` - current user wishlists (auth required)
- `GET /wishlist/{id}` - wishlist by id (auth required)
- `PUT /wishlist/{id}` - edit wishlist (auth required)
- `DELETE /wishlist/{id}` - delete wishlist (auth required)
- `POST /wishlist/access/{id}?user_id=<id>&role=<viewer|editor>` - grant/update access (auth required)
- `DELETE /wishlist/access/{id}?user_id=<id>` - revoke access (auth required)
- `GET /wishlist/access/{user_id}` - list access records for user
- `GET /wishlist/WishlistVisibility` - available visibility values
- `GET /wishlist/WishlistRole` - available role values

### Gifts
- `POST /wishlist/{wlid}/gifts` - create gift in wishlist (auth required)
- `GET /wishlist/{wlid}/gifts` - list gifts in wishlist (auth required)
- `GET /gifts/{gift_id}` - gift details (auth required)
- `PUT /gifts/{gift_id}` - edit gift fields (auth required)
- `DELETE /gifts/{gift_id}` - delete gift (auth required)

### Dev
- `GET /dev/health` - DB health check (auth required)
- `GET /dev/stats` - service stats (auth required)
- `GET /dev/wishlist` - list all wishlists (auth required)

## CORS
Allowed origins are configured in `src/main.py`:
- `http://localhost:5173`
- `http://127.0.0.1:5173`
- `https://dragledwl.ru`

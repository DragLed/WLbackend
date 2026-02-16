from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from authx.exceptions import AuthXException
from rout import users, gifts, auth
from database.database import engine, Base
import uvicorn




Base.metadata.create_all(bind=engine)
print("Tables created")

app = FastAPI(
    title="WLbackend",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "DragLed",
        "url": "http://t.me/DragLed",
        "email": "koren_mira.10@bk.ru",
    },
)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.rout)
app.include_router(users.rout)
app.include_router(gifts.rout)


@app.exception_handler(AuthXException)
def authx_exception_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail": "Authorization required"},
    )



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

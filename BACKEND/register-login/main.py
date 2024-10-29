from fastapi import FastAPI
from routers.user_auth import user_auth
from SQL import models
from SQL.engine import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

app.include_router(user_auth)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

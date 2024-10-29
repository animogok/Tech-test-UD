from fastapi import APIRouter, HTTPException
from models.user import User
from SQL.engine import SessionLocal
from SQL.crud import get_user, post_user

user_auth = APIRouter()


@user_auth.post("/sign-in/")
async def login(email: str, password: str) -> str:
    user_db = get_user(db=SessionLocal(), user_email=email)
    if user_db.hashed_password == password:
        return "Login successful"
    else:
        return "Please check out your login credentials"


@user_auth.post("/sign-up/")
async def register(data: User) -> dict:
    if get_user(db=SessionLocal(), user_email=data.email):
        raise HTTPException(status_code=400, detail="This email it's used before")
    elif (data.age <= 18) or (data.age > 100):
        raise HTTPException(status_code=400, detail="You must be +18 years old")
    else:
        post_user(db=SessionLocal(), user_info=data)
        return {"Succes": "User have been created correctly"}

"""

This class shows the user functionality, this for the working login and register system

"""

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    surname: str
    age: int
    email: EmailStr
    wallet: int
    password: str

    class Config:
        orm_mode = True

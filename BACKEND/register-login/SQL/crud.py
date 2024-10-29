from sqlalchemy.orm import Session
from .models import UserDb
from models.user import User


def get_user(db: Session, user_email: str) -> User:
    return db.query(UserDb).filter(UserDb.email == user_email).first()


def post_user(db: Session, user_info: User) -> UserDb:
    # Create a UserDb instance from the Pydantic User data
    user_db = UserDb(
        name=user_info.name,
        surname=user_info.surname,
        email=user_info.email,
        wallet=str(user_info.wallet),  # Ensure wallet is a string
        hashed_password=user_info.password,  # You should ideally hash the password here
        is_active=True,  # Set active status if necessary
    )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalars().one_or_none()


def create_user(db: Session, email: str, password: str) -> User:
    user = User(email=email, password_hash=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.password_hash):
        return user
    return None


def create_token_for_user(user: User) -> str:
    return create_access_token(data={"sub": str(user.id)})

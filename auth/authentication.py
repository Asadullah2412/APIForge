from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth.utils import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
# from user_service import TokenData
# from model_d import User
from database.dependencies import model
from database.dependencies import db_dependency



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")



# def get_user(db: Session, username: str):
#     return db.query(User).filter(User.username == username).first()

def authenticate_user(db:db_dependency , username: str, password: str):
    user = db.scalars(
        select(model.User).where(model.User.user_name == username)
    ).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
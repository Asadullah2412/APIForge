from fastapi import APIRouter, HTTPException,Depends,status
from sqlalchemy import select
from pydantic import BaseModel
from database.dependencies import model
from database.dependencies import db_dependency
from auth.utils import get_password_hash , create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from auth.authentication import authenticate_user

class UserCreate(BaseModel):
    user_name:str
    password:str


UserRouter = APIRouter()

# add a new user
@UserRouter.post("/users")
async def signup(user_data :UserCreate,db:db_dependency):
    existing_user = db.scalars(select(model.User).where(model.User.user_name == user_data.user_name)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Already registered")
    hashed_password = get_password_hash(user_data.password)
    db_user = model.User(password = hashed_password,
                            user_name=user_data.user_name,
                            )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



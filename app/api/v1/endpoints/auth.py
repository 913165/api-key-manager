# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app.core.security import (
   verify_password,
   create_access_token,
   pwd_context,
   get_password_hash
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.token import Token

router = APIRouter()

@router.post("/signup", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> Any:
   db_user = db.query(User).filter(User.email == user.email).first()
   if db_user:
       raise HTTPException(status_code=400, detail="Email already registered")
   db_user = User(
       email=user.email,
       hashed_password=get_password_hash(user.password),
       first_name=user.first_name,
       last_name=user.last_name
   )
   db.add(db_user)
   db.commit()
   db.refresh(db_user)
   return db_user

@router.post("/token", response_model=Token)
def login(
   form_data: OAuth2PasswordRequestForm = Depends(),
   db: Session = Depends(get_db)
) -> Any:
   user = db.query(User).filter(User.email == form_data.username).first()
   if not user or not verify_password(form_data.password, user.hashed_password):
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Incorrect email or password",
           headers={"WWW-Authenticate": "Bearer"},
       )
   return {
       "access_token": create_access_token(user.id),
       "token_type": "bearer"
   }
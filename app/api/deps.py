# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from uuid import UUID

from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import get_db, SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        # Parse the UUID before querying
        user_uuid = UUID(user_id)
        user = db.query(User).filter(User.id == user_uuid).first()
        if user is None:
            raise credentials_exception
        return user
    except (JWTError, ValueError):
        raise credentials_exception


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
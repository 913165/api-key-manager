# app/core/security.py
from datetime import datetime, timedelta
import secrets
import string
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_api_key() -> tuple[str, str]:
    """Generate a new API key and its hash"""
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for _ in range(32))
    api_key = f"sk_{api_key}"
    hashed_key = pwd_context.hash(api_key)
    return api_key, hashed_key


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Create JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_api_key() -> tuple[str, str]:
   """Generate a new API key and its hash"""
   alphabet = string.ascii_letters + string.digits
   api_key = ''.join(secrets.choice(alphabet) for _ in range(32))
   api_key = f"sk_{api_key}"
   hashed_key = pwd_context.hash(api_key)
   return api_key, hashed_key
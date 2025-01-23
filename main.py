from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
import secrets
import string
from datetime import datetime
from models import ApiKey, User
from database import get_db

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generate_api_key() -> str:
    """Generate a secure API key"""
    alphabet = string.ascii_letters + string.digits
    prefix = 'pk_'  # or 'sk_' for secret keys
    key = ''.join(secrets.choice(alphabet) for _ in range(32))
    return f"{prefix}{key}"


@app.post("/api/keys")
async def create_api_key(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Create a new API key for the authenticated user"""
    api_key = generate_api_key()

    # Store hashed version in database
    hashed_key = hash_key(api_key)  # Implement your hashing logic
    db_api_key = ApiKey(
        hashed_key=hashed_key,
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )

    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)

    # Return unhashed key (will only be shown once)
    return {"id": db_api_key.id, "api_key": api_key}


@app.get("/api/keys")
async def list_api_keys(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> List[dict]:
    """List all API keys for the authenticated user"""
    keys = db.query(ApiKey).filter(ApiKey.user_id == current_user.id).all()
    return [
        {
            "id": key.id,
            "created_at": key.created_at,
            "last_used": key.last_used,
            # Only return prefix for display
            "prefix": key.get_prefix()
        }
        for key in keys
    ]


@app.delete("/api/keys/{key_id}")
async def delete_api_key(
        key_id: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Delete an API key"""
    key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == current_user.id
    ).first()

    if not key:
        raise HTTPException(status_code=404, detail="API key not found")

    db.delete(key)
    db.commit()
    return {"status": "success"}
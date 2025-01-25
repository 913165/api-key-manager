# app/api/v1/endpoints/api_keys.py
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.security import generate_api_key
from app.db.session import get_db
from app.models.api_key import ApiKey
from app.schemas.api_key import ApiKeyCreate, ApiKeyResponse
from app.api.deps import get_current_user
import logging
router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/", response_model=ApiKeyResponse)
def create_api_key(
        api_key: ApiKeyCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    api_key_value, hashed_key = generate_api_key()
    prefix = api_key_value[:8]

    db_api_key = ApiKey(
        user_id=current_user.id,
        key_name=api_key.key_name,  # Updated to match schema
        hashed_key=hashed_key,
        prefix=prefix
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)

    return {
        "id": db_api_key.id,
        "key": api_key_value,
        "prefix": prefix,
        "key_name": db_api_key.key_name,
        "created_at": db_api_key.created_at,
        "is_active": db_api_key.is_active
    }


@router.get("/", response_model=List[ApiKeyResponse])
def list_api_keys(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    # Log debug information
    logger.debug(f"Current user ID: {current_user.id}")

    # Perform the query
    api_keys = db.query(ApiKey).filter(ApiKey.user_id == current_user.id).all()

    return api_keys


@router.delete("/{key_id}")
def delete_api_key(
        key_id: str,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == current_user.id
    ).first()

    if not key:
        raise HTTPException(status_code=404, detail="API key not found")

    db.delete(key)
    db.commit()
    return {"status": "success"}
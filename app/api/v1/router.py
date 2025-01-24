# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.api_keys import router as api_keys_router
from app.api.v1.endpoints.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth" ,tags=["auth"])
api_router.include_router(users_router,tags=["users"])
api_router.include_router(api_keys_router, prefix="/api-keys", tags=["api-keys"])
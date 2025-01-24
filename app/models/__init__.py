# app/models/__init__.py
from app.models.user import User
from app.models.api_key_log import ApiKeyLog  # Import this first
from app.models.api_key import ApiKey  # Then this

# Uncomment the Base.metadata.create_all line in main.py to create tables
from fastapi import APIRouter, HTTPException,Depends,status
import secrets
import hashlib
from database.dependencies import db_dependency
from auth.utils import get_current_user

apiServiceRouter = APIRouter()

def generate_api_key(prefix: str = "forge_") -> tuple[str, str]:
    """
    Generates a secure API key.
    Returns:
        (plain_text_key, hashed_key)
        - plain_text_key: Show this to the user ONCE.
        - hashed_key: Save this safely in your database.
    """
    # 1. Generate 32 bytes of secure random characters (64 hex characters)
    random_secret = secrets.token_hex(32)
    
    # 2. Combine prefix and secret to form the token
    plain_text_key = f"{prefix}{random_secret}"
    
    # 3. Create a SHA-256 hash of the complete key
    hashed_key = hashlib.sha256(plain_text_key.encode("utf-8")).hexdigest()
    
    return plain_text_key, hashed_key

# # Example Usage when a user clicks "Generate Key" on your dashboard:
# plain_key, db_hash = generate_api_key()

# print(f"DISPLAY TO USER (ONLY ONCE!): {plain_key}")
# print(f"SAVE IN DATABASE STORAGE    : {db_hash}")


@apiServiceRouter.post("/APIKey")
def create_new_api_key(db:db_dependency,   User = Depends(get_current_user)):
    plain_text_key,hashed_key = generate_api_key()

    user = db.get(User)
    user.apiKeys = hashed_key
    db.commit()
    db.refresh(user)

    return{
        "api_key": plain_text_key, 
        "note": "Copy this key now. You will not be able to see it again!"
    }







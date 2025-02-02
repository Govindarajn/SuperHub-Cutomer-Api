from common.database.models.user import User
from common.database.mongodb import db
from common.auth.password import hash_password, verify_password
from typing import List, Optional
from datetime import datetime

async def create_user(username: str, email: str, password: str, role: str) -> User:
    hashed_password = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        role=role,
        created_at=datetime.utcnow(),
    )
    result = await db["users"].insert_one(new_user.dict())
    new_user.id = str(result.inserted_id)
    return new_user

async def get_user_by_id(user_id: str) -> Optional[User]:
    user = await db["users"].find_one({"_id": user_id})
    if user:
        return User(**user)
    return None

async def authenticate_user(email: str, password: str) -> Optional[str]:
    user = await db["users"].find_one({"email": email})
    if user and verify_password(password, user["password"]):
        return str(user["_id"])  # Return user_id as JWT payload
    return None

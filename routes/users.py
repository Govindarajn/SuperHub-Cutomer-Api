from fastapi import APIRouter, Depends, HTTPException
from common.database.models.user import User
from customer-api.services.user_service import create_user, get_user_by_id
from typing import List

router = APIRouter()

@router.post("/create", response_model=User)
async def create_new_user(user: User):
    existing_user = await get_user_by_id(user.id)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return await create_user(user.username, user.email, user.password, user.role)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

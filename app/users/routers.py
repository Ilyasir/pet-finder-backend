from fastapi import APIRouter, HTTPException
from app.users.schemas import SUserBase, SUserCreate, SUserResponse
from app.users.services import UserService

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/", response_model=list[SUserResponse])
async def get_users():
    users = await UserService.find_all()
    return users

@router.get("/{user_id}", response_model=SUserResponse)
async def get_user(user_id: int):
    user = await UserService.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
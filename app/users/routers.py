from fastapi import APIRouter, HTTPException, Response, Depends
from app.users.schemas import SUserLogin, SUserCreate, SUserResponse
from app.users.services import UserService
from app.users.models import User
from app.users.auth import get_password_hash, create_access_token, authenticate_user
from app.users.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/", response_model=list[SUserResponse])
async def get_users():
    users = await UserService.find_all()
    return users

@router.get("/me", response_model=SUserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=SUserResponse)
async def get_user(user_id: int):
    user = await UserService.find_one_or_none(id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.post("/register", status_code=201)
async def register_user(user_data: SUserCreate):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(email=user_data.email, hashed_password=hashed_password)
    return {"detail": "Пользователь зарегистрирован"}


@router.post("/login")
async def login_user(response: Response, user_data: SUserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    access_token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
    key="pets_access_token",
    value=access_token,
    httponly=True,
    samesite="lax",
    max_age=3600)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("pets_access_token")
    return {"detail": "Пользователь вышел"}
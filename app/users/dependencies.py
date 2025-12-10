from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime
from typing import Optional

from app.config import settings
from app.users.services import UserService


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("pets_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен отсутствует",
        )
    return token


async def get_current_user(token: str = Depends(get_token_from_cookie)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")

    exp = payload.get("exp")
    if not exp or int(exp) < int(datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истёк")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен (no sub)")

    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

    return user

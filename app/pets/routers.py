from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.pets.schemas import SPetCreate, SPetResponse, SPetUpdate
from app.pets.services import PetService
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/pets", tags=["Питомцы"])


@router.get("/", response_model=List[SPetResponse])
async def get_pets():
    return await PetService.find_all()


@router.get("/{pet_id}", response_model=SPetResponse)
async def get_pet(pet_id: int):
    pet = await PetService.find_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    return pet


@router.post("/", response_model=SPetResponse)
async def create_pet(pet: SPetCreate, current_user: User = Depends(get_current_user)):
    payload = pet.model_dump()
    payload["owner_id"] = current_user.id
    new_pet = await PetService.create_pet(payload)
    return new_pet


@router.put("/{pet_id}", response_model=SPetResponse)
async def update_pet(pet_id: int, pet_update: SPetUpdate, current_user: User = Depends(get_current_user)):
    """
    Обновление — только если текущий пользователь владелец.
    """
    pet_obj = await PetService.find_by_id(pet_id)
    if not pet_obj:
        raise HTTPException(status_code=404, detail="Питомец не найден")

    if pet_obj.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на изменение этого питомца")

    update_data = pet_update.model_dump(exclude_unset=True)
    updated = await PetService.update_pet(pet_id, update_data)
    return updated


@router.delete("/{pet_id}", status_code=status.HTTP_200_OK)
async def delete_pet(pet_id: int, current_user: User = Depends(get_current_user)):
    """
    Удаление — только владелец.
    """
    pet_obj = await PetService.find_by_id(pet_id)
    if not pet_obj:
        raise HTTPException(status_code=404, detail="Питомец не найден")

    if pet_obj.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на удаление этого питомца")

    ok = await PetService.delete_pet(pet_id)
    if not ok:
        raise HTTPException(status_code=500, detail="Ошибка при удалении")
    return {"detail": "Питомец удалён"}

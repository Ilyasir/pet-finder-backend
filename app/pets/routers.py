from fastapi import APIRouter, HTTPException
from app.pets.schemas import SPetCreate, SPetUpdate, SPetResponse
from app.pets.services import PetService

router = APIRouter(prefix="/pets", tags=["Питомцы"])

@router.get("/", response_model=list[SPetResponse])
async def get_pets():
    pets = await PetService.find_all()
    return pets

@router.get("/{pet_id}", response_model=SPetResponse)
async def get_pet(pet_id: int):
    pet = await PetService.find_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    return pet

@router.post("/", response_model=SPetResponse)
async def create_pet(pet: SPetCreate):
    new_pet = await PetService.create_pet(pet.model_dump())
    return new_pet

@router.put("/{pet_id}", response_model=SPetResponse)
async def update_pet(pet_id: int, pet: SPetUpdate):
    pet_data = pet.model_dump(exclude_unset=True)

    updated_pet = await PetService.update_pet(pet_id, pet_data)

    if not updated_pet:
        raise HTTPException(status_code=404, detail="Питомец не найден")

    return updated_pet

@router.delete("/{pet_id}")
async def delete_pet(pet_id: int):
    deleted = await PetService.delete_pet(pet_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Питомец не найден")

    return {"detail": "Питомец удалён"}

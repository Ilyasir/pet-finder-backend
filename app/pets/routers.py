from fastapi import APIRouter, HTTPException
from app.pets.schemas import SPetBase, SPetCreate, SPetResponse, SPetUpdate
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
    new_pet = await PetService.create_pet(pet.dict())
    return new_pet